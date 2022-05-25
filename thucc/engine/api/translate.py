#-*- coding: utf-8 -*-
import codecs
import json
import sys
import re
import os
import Levenshtein
import requests
import xml.etree.ElementTree as ET

from collections import OrderedDict

from thucc.engine.utils import log_solve

def translate(srcList):
    """
    Inputs: 
        srcList: [
            "使吴越，致命讫即还",
            "吾终拒之，是近名也",
            "邀煜入宫治装",
            "上觉，遽诘所以",
            "煜之君臣，卒赖保全。"
        ]
    
    Outputs:
        tgtList: [
            "出使吴越，到使命完成就立即还朝",
            "我将拒之，名称是近代",
            "李煜入宫邀请刻意整束行装",
            "皇上发现了，立即问什么原因",
            "李煜的君臣，终于依靠保全。"
        ]
    """
    single_flag = False
    if not isinstance(srcList, list):
        srcList = [srcList]
        single_flag = True
    url = "http://127.0.0.1:36789/translate/"
    ret = requests.post(url, json={'srcList': srcList})
    tgtList = eval(json.loads(ret.text))
    if single_flag:
        tgtList = tgtList[0]
    return tgtList

def pure(s):
	s = s.replace('\t','')
	s = s.replace('\n','')
	s = s.replace(' ','')
	s = s.replace('\r','')
	return s

@log_solve('translate')
def solve_translate(question):
    q_str = question.to_string()
    if re.search("解释.*(字面意思|含义)", q_str) is not None:
        t_str = re.search("“(.+)”", q_str).groups()[-1]
    else:
        t_str = question.node.find('text').text
    t_str = pure(t_str)
    
    res = translate([t_str])[0]
    outputs = {
        'ans': res
    }
    return outputs

@log_solve('translate')
def solve_tselect(question):
    srcList = []
    tgtList = []
    valueList = []
    for (value, text) in question.options:
        valueList.append(value)
        text = pure(text)
        srcList.append(text.split('$$')[0])
        tgtList.append(text.split('$$')[1])
    
    hypList = translate(srcList)
    
    mini = valueList[0]
    minD = 1e10
    maxi = valueList[0]
    maxD = -1e10

    explain = OrderedDict()
    explain['题目ID'] = question.qid
    explain['题型'] = '翻译选择题'
    explain['问题'] = question.text
    explain['选项'] = question.options
    explain['第一步，翻译各选项'] = hypList

    edit_distances = []
    
    for src, tgt, hyp, value in zip(srcList, tgtList, hypList, valueList):
        hyp = pure(hyp)
        d = Levenshtein.distance(tgt, hyp)
        edit_distances.append(f'{value}: “{src}”的译文“{hyp}”与选项中提供的译文“{tgt}”的编辑距离为{d}。')
        if d < minD:
            mini = value
            minD = d
        if d > maxD:
            maxi = value
            maxD = d

    explain['第二步，计算编辑距离'] = edit_distances
            
    if '不' in question.text:
        answer = maxi
        attr = '大'
    else:
        answer = mini
        attr = '小'
    
    explain['第三步，答案选择'] = f'选项{answer}的编辑距离最{attr}，故选{answer}。'
    
    outputs = {
        'ans': answer,
        'explain': explain
    }
    return outputs

if __name__ == '__main__':
    qs = json.loads(codecs.open(sys.argv[1], 'r', 'utf-8').read())
    ret = getMTAns(qs)
    outputfile = codecs.open(sys.argv[2], 'w', 'utf-8')
    outputfile.write(json.dumps(ret))
    outputfile.close()
