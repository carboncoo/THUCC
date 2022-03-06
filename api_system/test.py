# coding=UTF-8
import re
import time
import json
import requests

def test_celery(questions):
    # pending
    url = "http://127.0.0.1:5001/api/solve"

    question_queries = {}
    for k, question in questions.items():
        ret = requests.post(url, json=question)
        res = json.loads(ret.text)
        question_queries[k] = res

    # check loop
    check_url = "http://127.0.0.1:5001/api/check_result"
    running = list(question_queries.keys())
    while True:
        for k in running:
            res = question_queries[k]
            result = json.loads(requests.post(check_url, json=res).text)
            if result['status'] == 'processing':
                print(f'[{k}]: Processing...')
            else:
                print(f'[{k}]: {result}')
                running.remove(k)
        if running:
            time.sleep(5)
        else:
            return

if __name__ == '__main__':

    # data = {'test_insts': [['唯蕃能致焉', 3, '招致'], ['特为置一榻，去则县之', 8, '通“悬”，挂'], ['坐左转修武令', 1, '犯罪'], ['与五宫中郎将黄琬共典选举', 9, '典礼']], 'ask_correct': False, 'baihuas': ['吐蕃造成的只有能', '特地设置一副坐榻，徐稚离开后就把它悬挂起来', '在修武令同知枢密院事韩绍文为上京留守。', '与五宫中郎将黄琬共同掌管选择推举贤能之士的'], 'qtype': 'taggingjudge'}
    # url = "http://127.0.0.1:36792/wsd_translate_align"
    # ret = requests.post(url, json=data)
    # import ipdb; ipdb.set_trace()
    # res = json.loads(ret.text)
    # print(res)
    # exit()

    questions = {
        'wsd_a': {
            "question_id": "test01_06",
            "question_type": "选择题",
            "question": "下列对句中加点词语的解释，不正确的一项是__",
            "choices": [
                "唯蕃能**(point,0,Null)**致**(point,1,Null)**焉$$招致",
                "特为置一榻，去则**(point,0,Null)**县**(point,1,Null)**之$$通“悬”，挂",
                " **(point,0,Null)**坐**(point,1,Null)**左转修武令$$犯罪",
                "与五宫中郎将黄琬共**(point,0,Null)**典**(point,1,Null)**选举$$典礼",
            ]
        },
        'wsd_b': {
            "question_id": "test01_07",
            "question_type": "选择题",
            "question": "下列各组语句中加点的词，意义、用法都相同的一组是__",
            "choices": [
                "**(point,0,Null)**以**(point,1,Null)**父荫补秘书省校书郎$$**(point,0,Null)**以**(point,1,Null)**兵部郎中复知制诰",
                "**(point,0,Null)**故**(point,1,Null)**不次用卿$$职此**(point,0,Null)**故**(point,1,Null)**也",
                "吏有驰报**(point,0,Null)**者**(point,1,Null)**$$而州兵有谋起为应**(point,0,Null)**者**(point,1,Null)**",
                "举正潜捕首恶者斩**(point,0,Null)**之**(point,1,Null)**$$每进读及前代治乱**(point,0,Null)**之**(point,1,Null)**际",
            ]
        },
        'cc_tselect': {
            "question_id": "test01_08",
            "question_type": "翻译选择题",
            "question": "下列对文中语句的理解，不正确的一项是__",
            "choices": [
                "服阕，刺史周景辟别驾从事$$服丧期满，刺史周景召他为别驾从事",
                "言及反复，诚辞恳切$$反复申诉，词意肯切",
                "天下之士，莫不延颈想望太平$$天下之土无不伸长脖子盼望天下太平",
                "将官属诸生八十余人$$将官和学生八十余人",
            ]
        },
        'cc_uselect': {
            "question_id": "test01_09",
            "question_type": "文言文理解选择",
            "question": "下列对文中语句的理解，不正确的一项是__",
            "choices": []
        },
        'translate': {
            "question_id": "test01_10",
            "question_type": "翻译题",
            "question": "将下面语句译为现代汉语。",
            "text": "蕃因朝会，固理膺等。"
        },
        'cc_shortanswer': {
            "question_id": "test01_11",
            "question_type": "文言文简答题",
            "question": "陈蕃“终取灭亡之祸”的原因有哪些?请结合全文简要概括。",
            "passage": "陈蕃字仲举，汝南平舆人也。初仕郡，举孝廉，除郎中。遭母忧，弃官行丧，服阕，刺史周景辟别驾从事，以谏争不合，投传而去。太尉李固表荐，征拜议郎，再迁为乐安太守。时李膺为青州刺史，名有威政，属城闻风，皆自引去，蕃独以清绩留。郡人周璆，高洁之士。前后郡守招命莫肯至，唯蕃能致焉。字而不名，特为置一榻，去则县之。大将军梁冀威震天下，时遣书诣蕃，有所请托，不得通，使者诈求谒，蕃怒，笞杀之，坐左转修武令。稍迁，拜尚书。性方峻，不接宾客，士民亦畏其高。征为尚书令，送者不出郭门。延熹六年，车驾幸广成校猎。蕃上疏谏曰：“夫安平之时，尚宜有节，况当今之世，兵戎未戢，四方离散，是陛下焦心毁颜，坐以待旦之时也。又秋前多雨，民始种麦。今失其劝种之时，而令给驱禽除路之役，非贤圣恤民之意也。”书奏不纳。自蕃为光禄勋，与五官中郎将黄琬共典选举，不偏权富，而为势家郎所谮诉，坐免归。顷之，征为尚书仆射。八年，代杨秉为太尉。蕃让曰：“齐七政，训五典，臣不如议郎王畅。聪明亮达，文武兼姿，臣不如弛刑徒李膺。”帝不许。中常侍苏康、管霸等复被任用，遂排陷忠良，共相阿媚。大司农刘祐、河南尹李膺，皆以忤旨，为之抵罪。蕃因朝会，固理膺等，请加原宥，升之爵任。言及反复，诚辞恳切。帝不听，因流涕而起。窦后临朝，蕃与后父大将军窦武，同心尽力，征用名贤，共参政事，天下之士，莫不延颈想望太平。而帝乳母赵娆，旦夕在太后侧，中常侍曹节、王甫等与共交构，谄事太后。蕃常疾之，志诛中官，会窦武亦有谋。蕃因与窦武谋之，及事泄，曹节等矫诏诛武等。蕃时年七十余，闻难作，将官属诸生八十余人。并拔刃突入承明门，王甫遂令收蕃，即日害之。论曰：桓、灵之世，若陈蕃之徒，咸能树立风声，抗论惽俗。而驱驰崄厄之中，与刑人腐夫同朝争衡，终取灭亡之祸者，彼非不能洁情志也。愍夫世士以离俗为高，而人伦莫相恤也。以遁世为非义，故屡退而不去；以仁心为己任，虽道远而弥厉。功虽不终，然其信义足以携持民心。（《后汉书·陈藩传》，有删改）"
        },
        'analects': {
            "question_id": "test01_12_01",
            "question_type": "论语简答题",
            "question": "孔子说樊迟学稼、学为圃是个小人，却又承认自己多能鄙事，二者矛盾吗？你是如何理解的？",
            "passage": "太宰问于子贡曰：夫子圣者与？何其多能也？子贡曰：固天纵之将圣，又多能也。子闻之，曰：太宰知我乎？吾少也贱，故多能鄙事。君子多乎哉？不多也。樊迟请学稼，子曰：吾不如老农。请学为圃，曰：吾不如老圃。樊迟出。子曰：小人哉，樊须也上好礼，而民莫敢不敬；上好义，则民莫敢不服；上好信，则民莫敢不用情。夫如是，则四方之民襁负其子而至矣，焉用稼？"
        },
        'poem_uselect_a': {
            "question_id": "test01_13",
            "question_type": "古诗理解选择题",
            "question": "下列对文中语句的理解，不正确的一项是__",
            "choices": ["国家分裂自古都有，但外族入侵京城充满血腥的景象前所未闻，写出了战祸的惨烈。", "诗人回顾宗泽、岳飞两位军功卓著的抗金名将，体现了对他们的无比敬意。", "诗人运用想象，用上天悔祸，终将助力平虏，来暗示金兵对自己暴行的愧意。", "这首诗透露了陆游的报国之志，其思想与“早岁那知世事艰”篇有相同之处。"],
            "passage": "书愤 陆游\r\n山河自古有乖分，京洛腥膻实未闻。剧盗曾从宗父命，遗民犹望岳家军。上天悔祸终平虏，公道何人肯散群？白首自知疏报国，尚凭精意祝炉熏。"
        },
        'poem_uselect_b': {
            "question_id": "test01_14",
            "question_type": "古诗理解选择题",
            "question": "下列对文中语句的理解，不正确的一项是__",
            "choices": ["国家分裂自古都有，但外族入侵京城充满血腥的景象前所未闻，写出了战祸的惨烈。", "诗人回顾宗泽、岳飞两位军功卓著的抗金名将，体现了对他们的无比敬意。", "诗人运用想象，用上天悔祸，终将助力平虏，来暗示金兵对自己暴行的愧意。", "这首诗透露了陆游的报国之志，其思想与“早岁那知世事艰”篇有相同之处。"],
            "passage": "书愤 宋 陆游\r\n山河自古有乖分，京洛腥膻实未闻。剧盗曾从宗父命，遗民犹望岳家军。上天悔祸终平虏，公道何人肯散群？白首自知疏报国，尚凭精意祝炉熏。"
        },
        'short_answer': {
            "question_id": "test01_15",
            "question_type": "简答题",
            "question": "诗的颈联有何含意?从中可以看出作者怎样的态度?",
            "passage": "梅花$$张道洽$$行尽荒林一径苔，竹梢深处数枝开。绝知南雪羞相并，欲嫁东风耻自媒。无主野桥随月管，有根寒谷也春回。醉余不睡庭前地，只恐忽吹花落来。"
        },
        'dictation': {
            "question_id": "test01_16_01",
            "question_type": "简答题",
            "question": "在横线上填写作品原句。",
            "text": "黑格尔的“人类从历史中学到的唯一的教训，就是没有从历史中吸取到任何教训”佐证了杜牧在《阿房宫赋》中的“__，__”观点。"
        },
        'whole_book_writing': {
            "question_id": "test01_17",
            "question_type": "整本书阅读题",
            "question": "《红楼梦》中“宝黛初会”时宝玉有一个摔玉的举动，他摔玉的原因是什么？表明了他怎样的性格特征？",
        },
        'microwrite': {
            "question_id": "test01_23",
            "question_type": "微写作",
            "question": "从下面三个题目中任选一题，按要求作答。",
            "passage": [
                "语文老师请同学们推荐名著中的章节或片段供课上研读。假如让你推荐《三国演义》，你选择哪个章节或片段？请用一句话表述推荐内容，并简要陈述理由。200字左右。",
                "以“啊，好美的一条河”为开头，联系生活，描写一个画面。要求：运用至少两种修辞手法，写景动静结合，描写生动优美，200字左右。",
                "参照杜甫的画像，结合你对杜甫的了解，请你发挥联想与想象，对杜甫的画像作一番描绘。要求：运用第二人称，至少用一种修辞手法，200字左右。"
            ]
        }
    }
    questions = {
        # 'poem_uselect_a': questions['poem_uselect_a'],
        # 'poem_uselect_b': questions['poem_uselect_b']
        # 'dictation': questions['dictation'],
        # 'whole_book_writing': questions['whole_book_writing']
        # 'poem_uselect': questions['poem_uselect']
        'microwrite': questions['microwrite']
    }
    test_celery(questions)
