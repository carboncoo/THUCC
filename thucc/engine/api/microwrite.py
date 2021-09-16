import re
import json
import requests

def microwrite(prompts):
    """
    Inputs: 
        prompts: [
            "司马牛问君子... @@",
            "棘子成曰... @@"
        ]
    Outputs:
        generates: [
            "面对国家安危，他深知...",
            "“君子坦荡荡”“淡泊名利”是..."
        ]
    """
    url = "http://127.0.0.1:36790/microwrite"
    ret = requests.post(url, json={'prompts': prompts})
    return json.loads(ret.text)

not_chinese_pattern = u"[^\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa5]"

def pure(s):
    s = s.replace('\t','')
    s = s.replace('\n','')
    s = s.replace(' ','')
    s = s.replace('\r','')
    s = re.sub(not_chinese_pattern, "", s)
    return s

def solve_microwrite(question):
    prompts = [pure(question.text) + "@@"]
    res = microwrite(prompts)
    outputs = {
        'ans': res[0]
    }
    return outputs

def solve_wholebookreading_with_microwrite(question):
    prompts = [pure(question.text) + "@@"]
    res = microwrite(prompts)
    outputs = {
        'ans': res[0]
    }
    return outputs

def solve_poem_shortanswer_with_microwrite(question):
    context = question.questions.node.find("text").text
    title, writer, poem = context.strip().replace('\t', ' ').split()
    title, writer, poem = pure(title), pure(writer), pure(poem)
    qstem = pure(question.text)
    prompts = [
        f"{title}@@{writer}@@{poem}@@{qstem}@@"
    ]
    res = microwrite(prompts)
    outputs = {
        'ans': res[0]
    }
    return outputs

def solve_cc_shortanswer_with_microwrite(question):
    context = pure(question.questions.node.find("text").text)
    qstem = pure(question.text)
    prompts = [
        f"{context}@@{qstem}@@"
    ]
    res = microwrite(prompts)
    outputs = {
        'ans': res[0]
    }
    return outputs

def solve_analects_with_microwrite(question):
    context = pure(question.get_text(question.questions.node.find("text")))
    qstem = pure(question.text)
    prompts = [
        f"{context}@@{qstem}@@"
    ]
    res = microwrite(prompts)
    outputs = {
        'ans': res[0]
    }
    return outputs

