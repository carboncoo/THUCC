import os
import re
import time
from celery import Celery
from collections import OrderedDict

from engine_api import microwrite, dictation, poem_answer, translate, wsd_translate_align, poem_uselect, cc_answer

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

not_chinese_pattern = u"[^\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa5]"

def pure(s, only_chinese=True):
    s = s.replace('\t','')
    s = s.replace('\n','')
    s = s.replace(' ','')
    s = s.replace('\r','')
    if only_chinese:
        s = re.sub(not_chinese_pattern, "", s)
    return s


def clearmark(sent):
    # clear marks to get raw text
    return sent.replace('**(point,0,Null)**', '').replace('**(point,1,Null)**', '')

@celery.task(name='tasks.solve_wsd')
def solve_wsd(data):
    # determine wsd type
    point_mark = '**(point,0,Null)**'
    def is_sentence_pair_option(option):
        if '$$' not in option:
            return False
        part_a, part_b = option.split('$$')
        return point_mark in part_a and point_mark in part_b

    def is_tagging_option(option):
        if '$$' not in option:
            return False
        part_a, part_b = option.split('$$')
        return point_mark in part_a and point_mark not in part_b

    text = data['question']
    options = data['choices']
    example_option = options[0]
    qtype = None
    # if '解释' in headtext:
    #     qtype = 'tagging'
    if '解释' in text and is_tagging_option(example_option):
        qtype = 'taggingjudge'
    elif is_sentence_pair_option(example_option):
        qtype = 'sentence_pair'
    elif ('意义' in text or '用法' in text) and '$$' not in example_option:
        qtype = 'compare'

    ask_correct = False if "不" in text else True

    if qtype == 'taggingjudge':
        test_insts = []
        for option in options:
            sent, sense = option.split('$$')
            pos = sent.index('**(point,0,Null)**')
            sent = clearmark(sent).strip()
            test_insts.append([sent, pos, sense])
        baihuas = translate([test_inst[0] for test_inst in test_insts])
    elif qtype == 'sentence_pair':
        test_insts = []
        for option in options:
            sent_a, sent_b = option.split('$$')
            pos_a, pos_b = sent_a.index('**(point,0,Null)**'), sent_b.index('**(point,0,Null)**')
            sent_a, sent_b = clearmark(sent_a).strip(), clearmark(sent_b).strip()
            test_insts += [[sent_a, pos_a], [sent_b, pos_b]]
        baihuas = translate([test_inst[0] for test_inst in test_insts])
    elif qtype == 'compare':
        test_insts = []
        for option in options:
            sent = option
            pos = sent.index('**(point,0,Null)**')
            sent = clearmark(sent).strip()
            test_insts += [[sent, pos]]
        baihuas = translate([test_inst[0] for test_inst in test_insts])

    outputs = wsd_translate_align(test_insts, ask_correct, baihuas, qtype)

    outputs['answer'] = chr(65 + outputs.pop('ans'))

    explain = OrderedDict()
    explain['题目ID'] = data['question_id']
    explain['题型'] = '词义消歧题'
    explain['问题'] = data['question']
    explain['选项'] = options

    explain['第一步，翻译各选项'] = baihuas

    align_results = []

    if qtype == 'taggingjudge':
        for test_inst, option_result in zip(test_insts, outputs['explain'].strip().split('\n')):
            pointed_word = test_inst[0][test_inst[1]]
            _, aligned_desc, option_desc, score = option_result.split('\t')
            score = float(score)
            align_results.append(f'加点字“{pointed_word}”对齐得到的释义为“{aligned_desc}”，与选项中释义“{option_desc}”的对比得分为{score:.3f}')
    elif qtype == 'sentence_pair':
        for idx, option_result in enumerate(outputs['explain'].strip().split('\n')):
            pointed_word_a, pointed_word_b = test_insts[idx*2][0][test_insts[idx][1]], test_insts[idx*2+1][0][test_insts[idx+1][1]]
            baihua_a, desc_a, baihua_b, desc_b, score = option_result.split('. ')[1].split('\t')
            score = float(score)
            align_results.append(f'第一句中加点字“{pointed_word_a}”的释义为“{desc_a}”，第一句中加点字“{pointed_word_b}”的释义为“{desc_b}”, 两者对比得分为{score:.3f}')

    explain['第二步，对齐并计算得分'] = align_results
    explain['第三步，答案选择'] = f'根据各选项得分，选{outputs["answer"]}。'
    outputs['explain'] = explain
    
    return outputs

import Levenshtein
@celery.task(name='tasks.solve_cc_tselect')
def solve_cc_tselect(data):
    """
    data = {
        "question_id": "test01_08",
        "question_type": "翻译选择题",
        "question": "下列对文中语句的理解，不正确的一项是__",
        "choices": [
            "服阕，刺史周景辟别驾从事$$服丧期满，刺史周景召他为别驾从事",
            "言及反复，诚辞恳切$$反复申诉，词意肯切",
            "天下之士，莫不延颈想望太平$$天下之土无不伸长脖子盼望天下太平",
            "将官属诸生八十余人$$将官和学生八十余人",
        ]
    }
    """
    srcList = []
    tgtList = []
    valueList = [chr(65+i) for i in range(len(data['choices']))]
    for text in data['choices']:
        text = pure(text, only_chinese=False)
        srcList.append(text.split('$$')[0])
        tgtList.append(text.split('$$')[1])
    
    hypList = translate(srcList)
    
    mini = valueList[0]
    minD = 1e10
    maxi = valueList[0]
    maxD = -1e10

    explain = OrderedDict()
    explain['题目ID'] = data['question_id']
    explain['题型'] = '翻译选择题'
    explain['问题'] = data['question']
    explain['选项'] = data['choices']
    explain['第一步，翻译各选项'] = hypList

    edit_distances = []
    
    for src, tgt, hyp, value in zip(srcList, tgtList, hypList, valueList):
        hyp = pure(hyp)
        d = Levenshtein.distance(tgt, hyp)
        edit_distances.append(f'{value}: “{src}”的译文“{hyp}”与选项中提供的译文“{tgt}”的编辑距离为{d}。')
        if d < minD:
            mini = value
            minD = d
        if d > maxD:
            maxi = value
            maxD = d

    explain['第二步，计算编辑距离'] = edit_distances
            
    if '不' in data['question']:
        answer = maxi
        attr = '大'
    else:
        answer = mini
        attr = '小'
    
    explain['第三步，答案选择'] = f'选项{answer}的编辑距离最{attr}，故选{answer}。'
    
    outputs = {
        'answer': answer,
        'explain': explain
    }
    return outputs

@celery.task(name='tasks.solve_translate')
def solve_translate(data):
    """
    data = {
        "question_id": "test01_10",
        "question_type": "翻译题",
        "question": "将下面语句译为现代汉语。",
        "text": "蕃因朝会，固理膺等。"
    }
    """
    q_str = data['question']
    if re.search("解释.*(字面意思|含义)", q_str) is not None:
        t_str = re.search("“(.+)”", q_str).groups()[-1]
    else:
        t_str = data['text']
    t_str = pure(t_str, only_chinese=False)
    
    res = translate([t_str])[0]
    outputs = {
        'answer': res
    }
    return outputs

# @celery.task(name='tasks.solve_cc_shortanswer')
# def solve_cc_shortanswer(data):
#     """
#     data = {
#         "question_id": "test01_11",
#         "question_type": "文言文简答题",
#         "question": "陈蕃“终取灭亡之祸”的原因有哪些?请结合全文简要概括。",
#         "passage": "陈蕃字仲举，汝南平舆人也。初仕郡，举孝廉，除郎中。遭母忧，弃官行丧，服阕，刺史周景辟别驾从事，以谏争不合，投传而去。太尉李固表荐，征拜议郎，再迁为乐安太守。时李膺为青州刺史，名有威政，属城闻风，皆自引去，蕃独以清绩留。郡人周璆，高洁之士。前后郡守招命莫肯至，唯蕃能致焉。字而不名，特为置一榻，去则县之。大将军梁冀威震天下，时遣书诣蕃，有所请托，不得通，使者诈求谒，蕃怒，笞杀之，坐左转修武令。稍迁，拜尚书。性方峻，不接宾客，士民亦畏其高。征为尚书令，送者不出郭门。延熹六年，车驾幸广成校猎。蕃上疏谏曰：“夫安平之时，尚宜有节，况当今之世，兵戎未戢，四方离散，是陛下焦心毁颜，坐以待旦之时也。又秋前多雨，民始种麦。今失其劝种之时，而令给驱禽除路之役，非贤圣恤民之意也。”书奏不纳。自蕃为光禄勋，与五官中郎将黄琬共典选举，不偏权富，而为势家郎所谮诉，坐免归。顷之，征为尚书仆射。八年，代杨秉为太尉。蕃让曰：“齐七政，训五典，臣不如议郎王畅。聪明亮达，文武兼姿，臣不如弛刑徒李膺。”帝不许。中常侍苏康、管霸等复被任用，遂排陷忠良，共相阿媚。大司农刘祐、河南尹李膺，皆以忤旨，为之抵罪。蕃因朝会，固理膺等，请加原宥，升之爵任。言及反复，诚辞恳切。帝不听，因流涕而起。窦后临朝，蕃与后父大将军窦武，同心尽力，征用名贤，共参政事，天下之士，莫不延颈想望太平。而帝乳母赵娆，旦夕在太后侧，中常侍曹节、王甫等与共交构，谄事太后。蕃常疾之，志诛中官，会窦武亦有谋。蕃因与窦武谋之，及事泄，曹节等矫诏诛武等。蕃时年七十余，闻难作，将官属诸生八十余人。并拔刃突入承明门，王甫遂令收蕃，即日害之。论曰：桓、灵之世，若陈蕃之徒，咸能树立风声，抗论惽俗。而驱驰崄厄之中，与刑人腐夫同朝争衡，终取灭亡之祸者，彼非不能洁情志也。愍夫世士以离俗为高，而人伦莫相恤也。以遁世为非义，故屡退而不去；以仁心为己任，虽道远而弥厉。功虽不终，然其信义足以携持民心。（《后汉书·陈藩传》，有删改）"
#     }
#     """
#     prompts = [
#         pure(data['passage']) + '@@' + pure(data['question']) + '@@'
#     ]
#     res = microwrite(prompts)[0]
#     return {
#         'answer': res
#     }

@celery.task(name='tasks.solve_cc_shortanswer')
def solve_cc_shortanswer(data):
    """
    data = {
        "question_id": "test01_11",
        "question_type": "文言文简答题",
        "question": "陈蕃“终取灭亡之祸”的原因有哪些?请结合全文简要概括。",
        "passage": "陈蕃字仲举，汝南平舆人也。初仕郡，举孝廉，除郎中。遭母忧，弃官行丧，服阕，刺史周景辟别驾从事，以谏争不合，投传而去。太尉李固表荐，征拜议郎，再迁为乐安太守。时李膺为青州刺史，名有威政，属城闻风，皆自引去，蕃独以清绩留。郡人周璆，高洁之士。前后郡守招命莫肯至，唯蕃能致焉。字而不名，特为置一榻，去则县之。大将军梁冀威震天下，时遣书诣蕃，有所请托，不得通，使者诈求谒，蕃怒，笞杀之，坐左转修武令。稍迁，拜尚书。性方峻，不接宾客，士民亦畏其高。征为尚书令，送者不出郭门。延熹六年，车驾幸广成校猎。蕃上疏谏曰：“夫安平之时，尚宜有节，况当今之世，兵戎未戢，四方离散，是陛下焦心毁颜，坐以待旦之时也。又秋前多雨，民始种麦。今失其劝种之时，而令给驱禽除路之役，非贤圣恤民之意也。”书奏不纳。自蕃为光禄勋，与五官中郎将黄琬共典选举，不偏权富，而为势家郎所谮诉，坐免归。顷之，征为尚书仆射。八年，代杨秉为太尉。蕃让曰：“齐七政，训五典，臣不如议郎王畅。聪明亮达，文武兼姿，臣不如弛刑徒李膺。”帝不许。中常侍苏康、管霸等复被任用，遂排陷忠良，共相阿媚。大司农刘祐、河南尹李膺，皆以忤旨，为之抵罪。蕃因朝会，固理膺等，请加原宥，升之爵任。言及反复，诚辞恳切。帝不听，因流涕而起。窦后临朝，蕃与后父大将军窦武，同心尽力，征用名贤，共参政事，天下之士，莫不延颈想望太平。而帝乳母赵娆，旦夕在太后侧，中常侍曹节、王甫等与共交构，谄事太后。蕃常疾之，志诛中官，会窦武亦有谋。蕃因与窦武谋之，及事泄，曹节等矫诏诛武等。蕃时年七十余，闻难作，将官属诸生八十余人。并拔刃突入承明门，王甫遂令收蕃，即日害之。论曰：桓、灵之世，若陈蕃之徒，咸能树立风声，抗论惽俗。而驱驰崄厄之中，与刑人腐夫同朝争衡，终取灭亡之祸者，彼非不能洁情志也。愍夫世士以离俗为高，而人伦莫相恤也。以遁世为非义，故屡退而不去；以仁心为己任，虽道远而弥厉。功虽不终，然其信义足以携持民心。（《后汉书·陈藩传》，有删改）"
    }
    """
    prompts = [
        pure(data['question']) + '###'
    ]
    res = cc_answer(prompts)[0]
    return {
        'answer': res
    }

@celery.task(name='tasks.solve_analects')
def solve_analects(data):
    """
    data = {
        "question_id": "test01_12_01",
        "question_type": "论语简答题",
        "question": "孔子说樊迟学稼、学为圃是个小人，却又承认自己多能鄙事，二者矛盾吗？你是如何理解的？",
        "passage": "太宰问于子贡曰：夫子圣者与？何其多能也？子贡曰：固天纵之将圣，又多能也。子闻之，曰：太宰知我乎？吾少也贱，故多能鄙事。君子多乎哉？不多也。樊迟请学稼，子曰：吾不如老农。请学为圃，曰：吾不如老圃。樊迟出。子曰：小人哉，樊须也上好礼，而民莫敢不敬；上好义，则民莫敢不服；上好信，则民莫敢不用情。夫如是，则四方之民襁负其子而至矣，焉用稼？"
    }
    """
    prompts = [
        pure(data['passage']) + '@@' + pure(data['question']) + '@@'
    ]
    res = microwrite(prompts)[0]
    return {
        'answer': res
    }

@celery.task(name='tasks.solve_poem_shortanswer')
def solve_poem_shortanswer(data):
    """
    data = {
        "question_id": "test01_15",
        "question_type": "简答题",
        "question": "诗的颈联有何含意?从中可以看出作者怎样的态度?",
        "passage": "梅花$$张道洽$$行尽荒林一径苔，竹梢深处数枝开。绝知南雪羞相并，欲嫁东风耻自媒。无主野桥随月管，有根寒谷也春回。醉余不睡庭前地，只恐忽吹花落来。"
    }
    """
    prompts = [
        data['passage'].replace('$$', '。') + f"###{data['question']}###"
    ]
    res = poem_answer(prompts)[0]
    return {
        'answer': res
    }

@celery.task(name='tasks.solve_dictation')
def solve_dictation(data):
    """
    data = {
        "question_id": "test01_16_01",
        "question_type": "默写题",
        "question": "在横线上填写作品原句。",
        "text": "黑格尔的“人类从历史中学到的唯一的教训，就是没有从历史中吸取到任何教训”佐证了杜牧在《阿房宫赋》中的“__，__”观点。"
    }
    """
    prompts = [
        data['text'] + ' $$'
    ]
    res = dictation(prompts)[0]
    return {
        'answer': res
    }

@celery.task(name='tasks.solve_wholebookreading')
def solve_wholebookreading(data):
    prompts = [pure(data['question']) + "@@"]
    res = microwrite(prompts)[0]
    outputs = {
        'answer': res
    }
    return outputs


@celery.task(name='tasks.solve_microwrite')
def solve_microwrite(data):
    """
    data = {
        "question_id": "test01_23",
        "question_type": "微写作",
        "question": "从下面三个题目中任选一题，按要求作答。",
        "passage": [
            "语文老师请同学们推荐名著中的章节或片段供课上研读。假如让你推荐《三国演义》，你选择哪个章节或片段？请用一句话表述推荐内容，并简要陈述理由。200字左右。",
            "以“啊，好美的一条河”为开头，联系生活，描写一个画面。要求：运用至少两种修辞手法，写景动静结合，描写生动优美，200字左右。",
            "参照杜甫的画像，结合你对杜甫的了解，请你发挥联想与想象，对杜甫的画像作一番描绘。要求：运用第二人称，至少用一种修辞手法，200字左右。"
        ]
    }
    """
    prompts = [
        x + '@@' for x in data['passage']
    ]
    res = microwrite(prompts)
    # res = res[0]
    return {
        'answer': res
    }

@celery.task(name='tasks.poem_uselect')
def solve_poem_uselect(data):
    """
    data = {
        "question_id": "test01_13",
        "question_type": "古诗理解选择题",
        "question": "下列对文中语句的理解，不正确的一项是__",
        "choices": ["国家分裂自古都有，但外族入侵京城充满血腥的景象前所未闻，写出了战祸的惨烈。", "诗人回顾宗泽、岳飞两位军功卓著的抗金名将，体现了对他们的无比敬意。", "诗人运用想象，用上天悔祸，终将助力平虏，来暗示金兵对自己暴行的愧意。", "这首诗透露了陆游的报国之志，其思想与“早岁那知世事艰”篇有相同之处。"],
        "passage": "书愤 宋 陆游 山河自古有乖分，京洛腥膻实未闻。剧盗曾从宗父命，遗民犹望岳家军。上天悔祸终平虏，公道何人肯散群？白首自知疏报国，尚凭精意祝炉熏。"
    }
    """
    # contents = data["passage"].split('$$')
    # if len(contents) == 3:
    #     title, writer, poem = contents
    # elif len(contents) == 4:
    #     title, dynasty, writer, poem = contents
    # else:
    #     return {'error': "wrong passage."}
    # title, writer, poem = pure(title), pure(writer), pure(poem)

    context = data["passage"]
    contexts = context.strip().replace('\t', ' ').replace('\n', ' ').split()
    title, writer, poem = contexts[0], contexts[1], ''.join(contexts[2:])
    title, writer, poem = pure(title), pure(writer), pure(poem)
    
    uselect_question = {
        "question_id": data["question_id"],
        "is_correct": not ('不' in data["question"]),
        "choices": data["choices"],
        "title": title,
        "dynasty": "",
        "poet": writer,
        "poem": poem
    }
    res = poem_uselect(uselect_question)
    res['answer'] = res.pop('ans')
    return res

@celery.task(name='tasks.cc_uselect')
def solve_cc_uselect(data):
    """
    """
    return {
        'answer': 'C'
    }