import json
import time
import xml.etree.ElementTree as ET

def answer_question(question, outputs):
    node = question.node
    ans_elm = ET.Element('answer', attrib={'org': 'THU'})
    ans_elm.text = outputs['ans']
    node.append(ans_elm)

    if 'explain' in outputs:
        explain_elm = ET.Element('explain', attrib={'org': 'THU'})
        explain_elm.text = json.dumps(outputs['explain'], indent=4, separators=(',', ': '), ensure_ascii=False)
        node.append(explain_elm)

def log_solve(system='undefined', level='info'):
    def decorator(func):
        def wrapper(question, **kwargs):
            print(f'Question: {question.qid} | System: {system} | Func: {func.__name__}: ', end='')
            time_start = time.time()
            outputs = func(question, **kwargs)
            answer_question(question, outputs)
            time_end = time.time()
            print(f'{time_end-time_start:.2f} s')
            print(f'Answer: {outputs["ans"]}\n')
            return outputs
        return wrapper
    return decorator