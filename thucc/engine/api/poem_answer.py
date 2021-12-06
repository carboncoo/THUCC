import re
import json
import requests

from thucc.engine.utils import log_solve

def poem_answer(prompts):
    """
    Inputs: 
        prompts: [
            "梦李白。杜甫。浮云终日行，游子久不至。三夜频梦君，情亲见君意。告归常局促，苦道来不易。江湖多风波，舟楫恐失坠。出门搔白首，若负平生志。冠盖满京华，斯人独憔悴。孰云网恢恢，将老身反累。千秋万岁名，寂寞身后事。###分析本诗中“江湖”和“风波”含义。###",
            "书愤。陆游。山河自古有乖分，京洛腥膻实未闻。剧盗曾从宗父命，遗民犹望岳家军。上天悔祸终平虏，公道何人肯散群？白首自知疏报国，尚凭精意祝炉熏。###诗歌题为“书愤”，结合全诗分析诗人为何而“愤”。###",
        ]
    
    Outputs:
        generates: [
           '①“江湖”指飘泊不定的游子；②“风波”指险恶多变的政治环境；③“江湖”指险恶多变的政治形势；④“风波”指人生盛衰无常、变幻莫测的境遇。', 
           '①山河分裂之恨。中原沦陷，金兵一度进逼建康，作者痛心疾首又无可奈何，激愤之情溢于言表。②年华已逝之悲。“岁华销尽”“疏髯浑似雪”，表达年华老去、无法驰骋疆场的悲哀。③安定生活之念。“送老齑盐何处是？我缘应在吴兴”，词人生逢乱世，客居异乡，渴望能归老吴兴。④离别不舍之情。“故人相望若为情，别愁深夜雨”，词人想归老吴兴，但又对建康的老朋友依恋不舍，离愁别绪笼罩心头。'
        ]
    """
    url = "http://127.0.0.1:36795/poem_answer"
    ret = requests.post(url, json={'prompts': prompts})
    return json.loads(ret.text)

not_chinese_pattern = u"[^\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa5]"
def pure(s, only_chinese=True):
    s = s.replace('\t','')
    s = s.replace('\n','')
    s = s.replace(' ','')
    s = s.replace('\r','')
    if only_chinese:
        s = re.sub(not_chinese_pattern, "", s)
    return s

@log_solve('poem_answer')
def solve_poem_shortanswer(question):
    context = question.questions.node.find("text").text
    contexts = context.strip().replace('\t', ' ').replace('\n', ' ').split()
    title, writer, poem = contexts[0], contexts[1], ''.join(contexts[2:])
    title, writer, poem = pure(title), pure(writer), pure(poem)
    prompt = [title + '。' + writer + '。' + poem + '###' + question.text + '###']
    res = poem_answer(prompt)[0]
    outputs = {
        'ans': res
    }
    return outputs