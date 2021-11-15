import re
import os
import json
import sys
import requests
import subprocess

from thucc.engine.utils import log_solve

systems_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../systems')

# os.path.join(systems_path, 'poem_appreciation')

not_chinese_pattern = u"[^\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa5]"
def pure(s, only_chinese=True):
    s = s.replace('\t','')
    s = s.replace('\n','')
    s = s.replace(' ','')
    s = s.replace('\r','')
    if only_chinese:
        s = re.sub(not_chinese_pattern, "", s)
    return s

@log_solve('poem_appreciation')
def solve_poem_shortanswer_with_appreciation(question):
    context = question.questions.node.find("text").text
    contexts = context.strip().replace('\t', ' ').replace('\n', ' ').split()
    title, writer, poem = contexts[0], contexts[1], ''.join(contexts[2:])
    title, writer, poem = pure(title), pure(writer), pure(poem)
    res = subprocess.check_output(['python', f'{systems_path}/poem_appreciation/src/test.py', poem]).decode('utf-8').strip()
    outputs = {
        'ans': res
    }
    return outputs