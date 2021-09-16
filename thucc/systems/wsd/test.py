# coding=UTF-8
import json
import requests

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

def get_sense(baihua, wenyan, index):
    url = "http://127.0.0.1:36792/get_sense"
    data = {
        'baihua': baihua,
        'wenyan': wenyan,
        'index': index
    }
    ret = requests.post(url, json=data)
    res = json.loads(ret.text)
    return res

if __name__ == '__main__':
    
    # taggingjudge
    test_insts = [
        ["遂受而籍之以归", 3, "籍：登记造册"],
        ["太祖典禁旅", 2, "典：主管，掌管"],
        ["副帅潘美预以为贺", 4, "预：参与，加入"],
        ["仍赐白金万两", 0, "于是，又"],
    ]

    ask_correct = False

    baihuas = ['，龚遂接受了，登记清楚后拿回来', '太祖掌管禁卫亲军', '副帅潘美预先祝贺他', '又赐给他白金万两']

    print(wsd_translate_align(test_insts, ask_correct, baihuas, 'taggingjudge'))
    
    # sentence_pair
    test_insts = [
        ['以百玩之具罗于席', 0],
        ['吴越人以轻舟追遣之', 3],
        ['观其所取', 2],
        ['一无所受', 2],
        ['汝何故疏我', 1],
        ['吾何功哉', 1],
        ['彬之总师也', 1],
        ['上临哭之恸', 3]
    ]
    ask_correct = False
    baihuas = ['把许多玩具放在席子上', '吴越人用小船追来送他', '看他拿什么东西', '一无所受', '你为什么会疏远我', '我有什么功劳呢', '唐彬的统帅军队的', '上前去，哭的很悲痛']
    print(wsd_translate_align(test_insts, ask_correct, baihuas, 'sentence_pair'))

    # get_sense
    baihua = '把许多玩具放在席子上'
    wenyan = '以 百 玩 之 具 罗 于 席'
    index = 7
    print(get_sense(baihua, wenyan, index))
