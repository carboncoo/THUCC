# coding=UTF-8
import json
import requests

def test_microwrite(prompts):
    url = "http://127.0.0.1:36790/microwrite"
    ret = requests.post(url, json={'prompts': prompts})
    return json.loads(ret.text)

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


if __name__ == '__main__':
    # prompts = [
    #     "司马牛问君子，子曰：“君子不忧不惧。”曰：“不忧不惧，斯谓之君子已乎？”子曰：“内省不疚，夫何忧何惧？”（《论语•颜渊》）司马牛，相传为宋国大夫桓魋的弟弟；传说他的哥哥桓魋参与宋国叛乱，失败后逃跑，司马牛也被迫离宋逃亡到鲁。孔子认为君子应该具备怎样的心理品质？@@",
    #     "司马牛问君子，子曰：“君子不忧不惧。”曰：“不忧不惧，斯谓之君子已乎？”子曰：“内省不疚，夫何忧何惧？”（《论语•颜渊》）司马牛，相传为宋国大夫桓魋的弟弟；传说他的哥哥桓魋参与宋国叛乱，失败后逃跑，司马牛也被迫离宋逃亡到鲁。司马牛在生活中遇到了怎样的困扰？孔子的回答对你有怎样的启迪？@@",
    #     "棘子成曰：“君子质而已矣，何以文为？”子贡曰：“惜乎，夫子之说君子也！驷不及舌。文犹质也，质犹文也。虎豹之鞟犹犬羊之鞟。”（《论语。颜渊》）”礼为情貌者也，文为质饰者也。夫君子取情而去貌，好质而恶饰。夫恃貌而论情者，其情恶也；须饰而论质者，其质衰也。何以论之？和氏之璧，不饰以五采；隋侯之珠，不饰以银黄。其质至美，物不足以饰之。夫物之待饰而后行者，其质不美也。(《韩非子·解老》)孔子曰:“质胜文则野,文胜质则史,文质彬彬,然后君子。”(《论语·雍也》)根据以上三段文字,请简要概括棘子成、韩非子、孔子的文质观。@@",
    #     "棘子成曰：“君子质而已矣，何以文为？”子贡曰：“惜乎，夫子之说君子也！驷不及舌。文犹质也，质犹文也。虎豹之鞟犹犬羊之鞟。”（《论语。颜渊》）”礼为情貌者也，文为质饰者也。夫君子取情而去貌，好质而恶饰。夫恃貌而论情者，其情恶也；须饰而论质者，其质衰也。何以论之？和氏之璧，不饰以五采；隋侯之珠，不饰以银黄。其质至美，物不足以饰之。夫物之待饰而后行者，其质不美也。(《韩非子·解老》)孔子曰:“质胜文则野,文胜质则史,文质彬彬,然后君子。”(《论语·雍也》)比较三人的文质观,你更赞同谁的观点? 为什么?@@",
    # ]
    # tgtList = test_microwrite(prompts)
    # print(tgtList)

    prompts = [
        "在你阅读的文学名著中，总会有一个鼓舞你成长的“引路人”。请从《红岩》《平凡的世界》中选取一个这样的人物，写一段抒情文字或一首小诗，表达你对他（她）的崇敬之情。要求：感情真挚，富有文采150字左右。@@",
        "学校举办戏剧节，拟将经典名著《红楼梦》《呐喊》搬上舞台。作为戏剧社成员，请就你最想饰演的某一人物的个性化语言，说明你的表演设想及理由。要求：选例典型，说明具体，理由充分。180字左右。@@",
        "人们常用“百科全书”“里程碑”等，形象地评价经典文学作品。请从《论语》《边城》《老人与海》中任选一部，对其进行形象的评价（“百科全书”“里程碑”除外），并阐释理由。要求：评价恰当，阐释合理180字左右。@@"
    ]

    print(microwrite(prompts))