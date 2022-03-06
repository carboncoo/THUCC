import re
import json
import requests

from thucc.engine.utils import log_solve

def cc_answer(prompts):
    """
    Inputs: 
        prompts: [
            "虞国的灭亡给后人提供了哪些教训？请结合文本加以说明。###",
            "辛弃疾认为导致百姓为盗的原因是什么?提出了怎样的建议?请用自己的话简要说明。###",
            "阅读文章，请用自己的话简要概括王旦是一个怎样的人。###",
        ]
    
    Outputs:
        generates: [
           "①不尊师从道，任用奸佞。②重农抑商，残酷压榨百姓。③不尊贤爱才，任用奸佞。④不尊法纪，执法犯法。",
           "①田地不够肥美；②水患频繁；③百姓无地耕种。",
           "王旦是一个为达目的不择手段、为达私利不徇私情的人。王旦为达目的不择手段，为达私利不徇私情。王旦是一个为达目的不择手段、为达私利不徇私情的人。"
        ]
    """
    url = "http://127.0.0.1:36800/cc_answer"
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

@log_solve('cc_answer')
def solve_cc_shortanswer(question):
    prompt = [question.text + '###']
    res = cc_answer(prompt)[0]
    outputs = {
        'ans': res
    }
    return outputs