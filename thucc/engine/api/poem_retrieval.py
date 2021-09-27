import re
import json
import requests

from thucc.engine.utils import log_solve

def poem_retrieval(blank):
    """
    Inputs: 
        blank: "当我们来到乡村，见到“鸡犬相闻”的景象，会联想到陶渊明在《归园田居》中“_________，鸡鸣桑树颠”来表达对田园生活的赞美。"
    Outputs:
        ans: "狗吠深巷中"
    """
    url = "http://127.0.0.1:36793/poem_retrieval"
    ret = requests.post(url, json={'blank': blank})
    return json.loads(ret.text)

def pure(s):
    s = s.replace('\t','')
    s = s.replace('\n','')
    s = s.replace(' ','')
    s = s.replace('\r','')
    return s

@log_solve('poem_retrieval')
def solve_dictation(question):
    text = question.node.find("blank").text
    text = pure(text)
    res = poem_retrieval(text)
    outputs = {
        'ans': res
    }
    return outputs