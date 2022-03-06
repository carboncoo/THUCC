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
    print(prompts)
    single_flag = False
    if not isinstance(prompts, list):
        prompts = [prompts]
        single_flag = True
    url = "http://172.17.0.1:36790/microwrite"
    ret = requests.post(url, json={'prompts': prompts})
    res = json.loads(ret.text)
    if single_flag:
        res = res[0]
    return res

def poem_answer(prompts):
    """
    Inputs: 
        prompts: [
            "梦李白。杜甫。浮云终日行，游子久不至。三夜频梦君，情亲见君意。告归常局促，苦道来不易。江湖多风波，舟楫恐失坠。出门搔白首，若负平生志。冠盖满京华，斯人独憔悴。孰云网恢恢，将老身反累。千秋万岁名，寂寞身后事。###分析本诗中“江湖”和“风波”含义。###",
            "书愤。陆游。山河自古有乖分，京洛腥膻实未闻。剧盗曾从宗父命，遗民犹望岳家军。上天悔祸终平虏，公道何人肯散群？白首自知疏报国，尚凭精意祝炉熏。###诗歌题为“书愤”，结合全诗分析诗人为何而“愤”。###",
        ]
    
    Outputs:
        generates: [
           '①“江湖”指飘泊不定的游子；②“风波”指险恶多变的政治环境；③“江湖”指险恶多变的政治形势；④“风波”指人生盛衰无常、变幻莫测的境遇。', 
           '①山河分裂之恨。中原沦陷，金兵一度进逼建康，作者痛心疾首又无可奈何，激愤之情溢于言表。②年华已逝之悲。“岁华销尽”“疏髯浑似雪”，表达年华老去、无法驰骋疆场的悲哀。③安定生活之念。“送老齑盐何处是？我缘应在吴兴”，词人生逢乱世，客居异乡，渴望能归老吴兴。④离别不舍之情。“故人相望若为情，别愁深夜雨”，词人想归老吴兴，但又对建康的老朋友依恋不舍，离愁别绪笼罩心头。'
        ]
    """
    url = "http://172.17.0.1:36795/poem_answer"
    ret = requests.post(url, json={'prompts': prompts})
    return json.loads(ret.text)

def dictation(blanks):
    """
    Inputs: 
        blank: ["毕业典礼上，校长引用《游褒禅山记》中的“________，________”两句，勉励学生在成长路上竭诚尽志，努力拼搏，做到无怨无悔。 $$"]
    Outputs:
        ans: ["而世之奇伟、瑰怪、非常之观 常在于险远"]
    """
    url = "http://172.17.0.1:36794/dictation"
    ret = requests.post(url, json={'prompts': blanks})
    return json.loads(ret.text)

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
    url = "http://172.17.0.1:36789/translate/"
    ret = requests.post(url, json=srcList)
    tgtList = json.loads(ret.text)
    if single_flag:
        tgtList = tgtList[0]
    return tgtList

def wsd_translate_align(test_insts, ask_correct, baihuas, qtype):
    url = "http://172.17.0.1:36792/wsd_translate_align"
    data = {
        'test_insts': test_insts,
        'ask_correct': ask_correct,
        'baihuas': baihuas,
        'qtype': qtype
    }
    print(data)
    ret = requests.post(url, json=data)
    res = json.loads(ret.text)
    return res

def poem_uselect(question):
    """
    question = {
        "question_id": "test01_13",
        "is_correct": True,
        "choices": ["梦中李白的到来离去，都令杜甫感到局促不安。", "“苦道来不易”写出了行路艰辛，二人见面不易。", "“冠盖满京华”，写出了李白在长安的交游之广。", "“千秋万岁名”，体现出杜甫对李白极高的评价。"],
        "title": "梦李白",
        "dynasty": "唐",
        "poet": "杜甫",
        "poem": "浮云终日行，游子久不至。三夜频梦君，情亲见君意。告归常局促，苦道来不易。江湖多风波，舟楫恐失坠。出门搔白首，若负平生志。冠盖满京华，斯人独憔悴。孰云网恢恢，将老身反累。千秋万岁名，寂寞身后事。"
    }
    """
    url = "http://172.17.0.1:36796/poem_uselect"
    ret = requests.post(url, json={'question': question})
    return json.loads(ret.text)

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
    url = "http://172.17.0.1:36800/cc_answer"
    ret = requests.post(url, json={'prompts': prompts})
    return json.loads(ret.text)