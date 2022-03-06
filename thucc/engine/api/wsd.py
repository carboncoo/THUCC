import re
import json
import requests

from collections import OrderedDict

from .translate import translate
from thucc.engine.utils import log_solve

def wsd_translate_align(test_insts, ask_correct, baihuas, qtype):
    url = "http://127.0.0.1:36792/wsd_translate_align"
    data = {
        'test_insts': test_insts,
        'ask_correct': ask_correct,
        'baihuas': baihuas,
        'qtype': qtype
    }
    ret = requests.post(url, json=data)
    res = json.loads(ret.text)
    return res

def get_sense(wenyan, index, baihua=None):
    url = "http://127.0.0.1:36792/get_sense"
    if not baihua:
        baihua = translate(wenyan)
    wenyan = ' '.join(wenyan.replace(' ', ''))
    data = {
        'baihua': baihua,
        'wenyan': wenyan,
        'index': index
    }
    ret = requests.post(url, json=data)
    res = json.loads(ret.text)
    # return res
    return {
        'wenyan': wenyan,
        'index': index,
        'baihua': baihua,
        'res': res
    }

def determine_qtype(headtext, text, example_option):
    # sentence_pair_keywords = ['组句', '组语句', '组词语', '下列句子', '下列各句', '下列语句']
    point_mark = '**(point,0,Null)**'

    def is_sentence_pair_option(option):
        if '$$' not in option:
            return False
        part_a, part_b = option.split('$$')
        return point_mark in part_a and point_mark in part_b

    def is_tagging_option(option):
        if '$$' not in option:
            return False
        part_a, part_b = option.split('$$')
        return point_mark in part_a and point_mark not in part_b

    qtype = None
    if '解释' in headtext:
        qtype = 'tagging'
    elif '解释' in text and is_tagging_option(example_option):
        qtype = 'taggingjudge'
    elif is_sentence_pair_option(example_option):
        qtype = 'sentence_pair'
    elif ('意义' in text or '用法' in text) and '$$' not in example_option:
        qtype = 'compare'
    
    return qtype

def clearmark(sent):
    # clear marks to get raw text
    return sent.replace('**(point,0,Null)**', '').replace('**(point,1,Null)**', '')

@log_solve('wsd')
def solve_wsd(question):
    options = question.options
    values = [option[0] for option in options]
    headtext = question.node.find('headtext')
    if headtext:
        headtext = headtext.text
    else:
        headtext = ''
    text = question.text
    
    qtype = determine_qtype(headtext, text, options[0][1])
    ask_correct = False if "不" in text else True

    if qtype == 'taggingjudge':
        test_insts = []
        for option in options:
            sent, sense = option[1].split('$$')
            pos = sent.index('**(point,0,Null)**')
            sent = clearmark(sent).strip()
            test_insts.append([sent, pos, sense])
        baihuas = translate([test_inst[0] for test_inst in test_insts])
    elif qtype == 'sentence_pair':
        test_insts = []
        for option in options:
            sent_a, sent_b = option[1].split('$$')
            pos_a, pos_b = sent_a.index('**(point,0,Null)**'), sent_b.index('**(point,0,Null)**')
            sent_a, sent_b = clearmark(sent_a).strip(), clearmark(sent_b).strip()
            test_insts += [[sent_a, pos_a], [sent_b, pos_b]]
        baihuas = translate([test_inst[0] for test_inst in test_insts])
    elif qtype == 'compare':
        test_insts = []
        for option in options:
            sent = option[1]
            pos = sent.index('**(point,0,Null)**')
            sent = clearmark(sent).strip()
            test_insts += [[sent, pos]]
        baihuas = translate([test_inst[0] for test_inst in test_insts])


    outputs = wsd_translate_align(test_insts, ask_correct, baihuas, qtype)

    outputs['ans'] = values[outputs['ans']]

    explain = OrderedDict()
    explain['题目ID'] = question.qid
    explain['题型'] = '词义消歧题'
    explain['问题'] = question.text
    explain['选项'] = question.options

    explain['第一步，翻译各选项'] = baihuas

    align_results = []

    if qtype == 'taggingjudge':
        for test_inst, option_result in zip(test_insts, outputs['explain'].strip().split('\n')):
            pointed_word = test_inst[0][test_inst[1]]
            _, aligned_desc, option_desc, score = option_result.split('\t')
            score = float(score)
            align_results.append(f'加点字“{pointed_word}”对齐得到的释义为“{aligned_desc}”，与选项中释义“{option_desc}”的对比得分为{score:.3f}')
    elif qtype == 'sentence_pair':
        for idx, option_result in enumerate(outputs['explain'].strip().split('\n')):
            pointed_word_a, pointed_word_b = test_insts[idx*2][0][test_insts[idx*2][1]], test_insts[idx*2+1][0][test_insts[idx*2+1][1]]
            baihua_a, desc_a, baihua_b, desc_b, score = option_result.split('. ')[1].split('\t')
            score = float(score)
            align_results.append(f'第一句中加点字“{pointed_word_a}”的释义为“{desc_a}”，第一句中加点字“{pointed_word_b}”的释义为“{desc_b}”, 两者对比得分为{score:.3f}')

    explain['第二步，对齐并计算得分'] = align_results
    explain['第三步，答案选择'] = f'根据各选项得分，选{outputs["ans"]}。'
    outputs['explain'] = explain
    
    return outputs