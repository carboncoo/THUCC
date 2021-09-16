import re
import json
import requests

from .translate import translate

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
        # baihuas = ['，龚遂接受了，登记清楚后拿回来', '太祖掌管禁卫亲军', '副帅潘美预先祝贺他', '又赐给他白金万两']
    elif qtype == 'sentence_pair':
        test_insts = []
        for option in options:
            sent_a, sent_b = option[1].split('$$')
            pos_a, pos_b = sent_a.index('**(point,0,Null)**'), sent_b.index('**(point,0,Null)**')
            sent_a, sent_b = clearmark(sent_a).strip(), clearmark(sent_b).strip()
            test_insts += [[sent_a, pos_a], [sent_b, pos_b]]
        baihuas = translate([test_inst[0] for test_inst in test_insts])
        # baihuas = ['把许多玩具放在席子上', '吴越人用小船追来送他', '看他拿什么东西', '一无所受', '你为什么会疏远我', '我有什么功劳呢', '唐彬的统帅军队的', '上前去，哭的很悲痛']
    elif qtype == 'compare':
        test_insts = []
        for option in options:
            sent = option[1]
            pos = sent.index('**(point,0,Null)**')
            sent = clearmark(sent).strip()
            test_insts += [[sent, pos]]
        baihuas = translate([test_inst[0] for test_inst in test_insts])
        # baihuas = ['把许多玩具放在席子上', '吴越人用小船追来送他', '看他拿什么东西', '一无所受', '你为什么会疏远我', '我有什么功劳呢', '唐彬的统帅军队的', '上前去，哭的很悲痛']

    outputs = wsd_translate_align(test_insts, ask_correct, baihuas, qtype)
    outputs['ans'] = values[outputs['ans']]
    
    return outputs