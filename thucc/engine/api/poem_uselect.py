import re
import json
import requests

from thucc.engine.utils import log_solve

def poem_uselect(question):
    """
    question = {
        "question_id": "test01_13",
        "is_correct": True,
        "choices": ["梦中李白的到来离去，都令杜甫感到局促不安。", "“苦道来不易”写出了行路艰辛，二人见面不易。", "“冠盖满京华”，写出了李白在长安的交游之广。", "“千秋万岁名”，体现出杜甫对李白极高的评价。"],
        "title": "梦李白",
        "dynasty": "唐",
        "poet": "杜甫",
        "poem": "浮云终日行，游子久不至。三夜频梦君，情亲见君意。告归常局促，苦道来不易。江湖多风波，舟楫恐失坠。出门搔白首，若负平生志。冠盖满京华，斯人独憔悴。孰云网恢恢，将老身反累。千秋万岁名，寂寞身后事。"
    }
    """
    url = "http://127.0.0.1:36796/poem_uselect"
    ret = requests.post(url, json={'question': question})
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

@log_solve('poem_uselect')
def solve_poem_uselect(question):
    context = question.questions.node.find("text").text
    contexts = context.strip().replace('\t', ' ').replace('\n', ' ').split()
    title, writer, poem = contexts[0], contexts[1], ''.join(contexts[2:])
    title, writer, poem = pure(title), pure(writer), pure(poem)
    dynasty = ""
    uselect_question = {
        "question_id": question.qid,
        "is_correct": not ('不' in question.text),
        "choices": [option[1] for option in question.options],
        "title": title,
        "dynasty": dynasty,
        "poet": writer,
        "poem": poem
    }
    return poem_uselect(uselect_question)