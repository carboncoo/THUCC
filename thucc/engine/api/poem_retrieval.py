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

def dictation(blanks):
    """
    Inputs: 
        blank: ["毕业典礼上，校长引用《游褒禅山记》中的“________，________”两句，勉励学生在成长路上竭诚尽志，努力拼搏，做到无怨无悔。 $$"]
    Outputs:
        ans: ["而世之奇伟、瑰怪、非常之观 常在于险远"]
    """
    url = "http://127.0.0.1:36794/dictation"
    ret = requests.post(url, json={'prompts': blanks})
    return json.loads(ret.text)

def api_dictation(blank):
    blank = pure(blank)
    res = poem_retrieval(blank)
    if res == '':
        res = dictation([blank + ' $$'])[0]
    return res

def pure(s):
    s = s.replace('\t','')
    s = s.replace('\n','')
    s = s.replace(' ','')
    s = s.replace('\r','')
    return s

def solve_dictation_with_dictation(question):
    text = question.node.find("blank").text
    text = pure(text) + " $$"
    res = dictation([text])[0]
    outputs = {
        'ans': res
    }
    return outputs

def solve_dictation_with_retrieval(question):
    text = question.node.find("blank").text
    text = pure(text)
    res = poem_retrieval(text)
    outputs = {
        'ans': res
    }
    return outputs

@log_solve('joint<poem_retrieval, dictation>')
def solve_dictation(question):
    outputs = solve_dictation_with_retrieval(question)
    if outputs['ans'] == '':
        outputs = solve_dictation_with_dictation(question)
    return outputs

@log_solve('poem_retrieval')
def solve_dictation_v1(question):
    return solve_dictation_with_retrieval(question)