import re
import json
import requests

from thucc.engine.utils import log_solve

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
    print(prompts)
    single_flag = False
    if not isinstance(prompts, list):
        prompts = [prompts]
        single_flag = True
    url = "http://127.0.0.1:36790/microwrite"
    ret = requests.post(url, json={'prompts': prompts})
    res = json.loads(ret.text)
    if single_flag:
        res = res[0]
    return res

not_chinese_pattern = u"[^\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa5]"
label_pattern = "\*\*.*?\*\*(.*?)\*\*.*?\*\*" # **(label,0,23_1)**
ord_pattern = u"([\u2460-\u2473])" # ① - ⑳

def pure(s, only_chinese=True):
    s = s.replace('\t','')
    s = s.replace('\n','')
    s = s.replace(' ','')
    s = s.replace('\r','')
    if only_chinese:
        s = re.sub(not_chinese_pattern, "", s)
    return s

@log_solve('microwrite')
def solve_microwrite(question):
    # context = pure(question.text)
    # prompts = [context + "@@"]
    
    # context = pure(question.text, only_chinese=False)
    # cnt = 0
    # replace special tokens
    # while re.search(label_pattern, context):
    #     cnt += 1 
    #     context = re.sub(label_pattern, f'（{cnt}）\\1', context, 1)
    # context = re.sub(ord_pattern, lambda x: "（{}）".format(ord(x.group(0))-9311), context)

    contexts = re.findall(label_pattern, question.text)
    prompts = [context + "@@" for context in contexts]
    res = microwrite(prompts)
    outputs = {
        'ans': res
    }
    return outputs

@log_solve('microwrite')
def solve_wholebookreading_with_microwrite(question):
    prompts = [pure(question.text) + "@@"]
    res = microwrite(prompts)
    outputs = {
        'ans': res[0]
    }
    return outputs

@log_solve('microwrite')
def solve_poem_shortanswer_with_microwrite(question):
    context = question.questions.node.find("text").text
    contexts = context.strip().replace('\t', ' ').replace('\n', ' ').split()
    title, writer, poem = contexts[0], contexts[1], ''.join(contexts[2:])
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

@log_solve('microwrite')
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

@log_solve('microwrite')
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

