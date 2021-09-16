import six
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass

class Question(object):

    def __init__(self, et, questions, section):
        self._xml_path = "section/questions/question"
        self._node = et
        self._id = et.attrib["id"]
        self._questions = questions
        self._section = section
        self._text = et.find("text")

        if self._text is not None:
            self._text = self._text.text
        
        self._options = []
        if self._node.attrib["type"] == "select":
            for op in self._node.findall('select/option'):
                self._options.append((op.attrib["value"], op.text))
        else:
            self._options = None

    @property
    def qid(self):
        return self._id

    @property
    def text(self):
        return self._text

    @property
    def node(self):
        return self._node

    @property
    def path(self):
        return self._xml_path

    @property
    def parent(self):
        return self._questions

    @property
    def questions(self):
        return self._questions

    @property
    def section(self):
        return self._section
    
    def to_string(self):
        return ET.tostring(self._node, encoding="utf-8").decode("utf-8")

    @property
    def options(self):
        return self._options

    @staticmethod
    def get_text(elem):
        if type(elem) in [Question, Questions, Section]:
            elem = elem.node
        texts = []

        if elem.text is not None:
            texts.append(elem.text)

        for e in elem:
            texts.append(get_text(e))

        return "\n".join(texts)
        

class Questions(object):

    def __init__(self, et, section):
        self._xml_path = "section/questions"
        self._id = et.attrib["id"]
        self._node = et
        self._section = section
        self._questions = {}

        questions = et.findall("question")

        for q in questions:
            qid = q.attrib["id"]
            self._questions[qid] = Question(q, self, section)

    @property
    def path(self):
        return self._xml_path

    @property
    def qid(self):
        return self._id

    @property
    def node(self):
        return self._node

    @property
    def parent(self):
        return self._section

    @property
    def questions(self):
        return six.itervalues(self._questions)

    @property
    def section(self):
        return self._section
    
    def to_string(self):
        return ET.tostring(self._node, encoding="utf-8").decode("utf-8")


class Section(object):

    def __init__(self, et):
        self._xml_path = "section"
        self._id = et.attrib["name"]
        self._node = et
        self._questions = {}

        questions = et.findall("questions")

        for q in questions:
            qid = q.attrib["id"]
            self._questions[qid] = Questions(q, self)

    @property
    def path(self):
        return self._xml_path

    @property
    def sid(self):
        return self._id

    @property
    def node(self):
        return self._node

    @property
    def questions(self):
        question_list = []

        for key in self._questions:
            questions = self._questions[key]
            question_list.extend(questions.questions)

        return question_list
    
    def to_string(self):
        return ET.tostring(self._node, encoding="utf-8").decode("utf-8")
    

def get_text(elem):
    if type(elem) in [Question, Questions, Section]:
        elem = elem.node
    texts = []

    if elem.text is not None:
        texts.append(elem.text)

    for e in elem:
        texts.append(get_text(e))

    return "\n".join(texts)

def match_text_or(text, regexps):
    if not isinstance(text, str):
        text = get_text(text)
    for regexp in regexps:
        if re.search(regexp, text) is not None:
            return True

    return False


def match_text_and(text, regexps, nflag=None):
    if not isinstance(text, str):
        text = get_text(text)
    results = []

    for regexp in regexps:
        if re.search(regexp, text) is not None:
            results.append(True)
        else:
            results.append(False)

    for i in range(len(results)):
        if nflag:
            if nflag[i] is True:
                results[i] = not results[i]

    return all(results)


def find_questions(sdict, keyword):
    for key in sdict:
        section = sdict[key]
        if match_text_or(section, keyword):
            return section.questions

    for key in sdict:
        section = sdict[key]
        questions = section.questions

        for question in questions:
            if match_text_or(question, keyword):
                return sdict[question.section].questions


def get_classic_questions(sdict):
    for key in sdict:
        section = sdict[key]
        if match_text_and(section, ["文言文"]):
            return section.questions


def get_poem_questions(sdict):
    for key in sdict:
        section = sdict[key]
        if match_text_and(section, ["诗", "诗句"]):
            return section.questions
        

def get_writing_questions(sdict):
    for key in sdict:
        section = sdict[key]
        if match_text_and(section, ["微写作"]):
            return section.questions


question_types = ['wsd',                # 题型：词义消歧 (6, 7)
                  'cc_tselect',         # 题型：翻译选择 (8)
                  'cc_uselect',         # 题型：文言文理解性选择 (9)
                  'translate',          # 题型：翻译 (10)
                  'cc_shortanswer',     # 题型：文言文简答（11）
                  'analects',           # 题型：论语（12, 13）
                  
                  'poem_uselect',       # 题型：诗歌理解性选择 (13, 14)
                  'poem_shortanswer',   # 题型：诗歌简答 (15)
                  'dictation',          # 题型：默写 (16)
                  'whole_book_reading', # 题型：整本书阅读（17）
                  
                  'microwrite'          # 题型：微写作（23）
                  ]


def determine_question_type(section_type, q):
    if section_type == 'cc':
        if q.node.attrib["type"] == "select":
            
            if match_text_and(q, [r"\*\*\(point,0,Null\)\*\*|<point>",
                                       "加点|划线", "词"]):
                return 'wsd' # 题型：词义消歧 (6, 7)
            
            elif match_text_and(q.node.find("text").text,
                              ["句", "解释|理解|译", "词"],
                              [False, False, True]):
                return 'cc_tselect' # 题型：翻译选择 (8)
            
            elif match_text_and(q.node.find("text").text, ["理解|分析", "句"],
                                                     [False, True]):
                return 'cc_uselect' # 题型：文言文理解性选择 (9)
        elif q.node.attrib["type"] == "shortanswer":
            if match_text_or(q, ["翻译", "译", "解释.*(字面意思|含义)"]):
                return 'translate' # 题型：翻译 (10)
            elif int(q.questions.node.attrib['score']) > 10:
                return 'cc_shortanswer' # 题型：文言文简答（11）
            else:
                return 'analects' # 题型：论语（12, 13）
            
    elif section_type == 'poem':
        
        if q.node.attrib["type"] == "select":
            return 'poem_uselect' # 题型：诗歌理解性选择 (13, 14)
        
        elif q.node.attrib["type"] == "fillblank":
            return 'dictation' # 题型：默写 (16)
        
        else: # shortanswer
            if q.questions.qid == 'questions_07':
                return 'whole_book_reading' # 整本书阅读（17）
            else:
                return 'poem_shortanswer' # 题型：诗歌简答 (15)
            
    elif section_type == 'writing':
        if match_text_and(q, ["微写作"]):
            return 'microwrite' # 题型：微写作（23）
    else:
        return None

def parse(filename):
    et = ET.parse(filename)
    section_list = et.findall("section")
    s_dict = {}

    for s in section_list:
        section = Section(s)
        s_dict[section.sid] = section
    
    mapping = {}
    for key in question_types:
        mapping[key] = []
    
    cc_questions = get_classic_questions(s_dict)
    for question in cc_questions:
        qtype = determine_question_type('cc', question)
        if qtype:
            mapping[qtype].append(question)
    
    poem_questions = get_poem_questions(s_dict)
    for question in poem_questions:
        qtype = determine_question_type('poem', question)
        if qtype:
            mapping[qtype].append(question)
            
    writing_questions = get_writing_questions(s_dict)
    for question in writing_questions:
        qtype = determine_question_type('writing', question)
        if qtype:
            mapping[qtype].append(question)

    for k in mapping:
        print(f'Question Type: [{k}]')
        for q in mapping[k]:
            print(q.qid)
        print()

    return mapping


if __name__ == '__main__':
    tq_mapping = parse("/data/private/cc/experiment/guwen_831/I.xml")
    
    for q in tq_mapping['cc_tselect']:
        import ipdb; ipdb.set_trace()
