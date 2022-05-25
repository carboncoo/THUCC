# coding=UTF-8
import json
import requests

def poem_retrieval(blank):
    """
    Inputs: 
        blank: "当我们来到乡村，见到“鸡犬相闻”的景象，会联想到陶渊明在《归园田居》中“_________，鸡鸣桑树颠”来表达对田园生活的赞美。"
    Outputs:
        ans: "狗吠深巷中"
    """
    url = "http://127.0.0.1:36793/poem_retrieval"
    ret = requests.post(url, json={'blank': blank})
    return json.loads(ret.text)

if __name__ == '__main__':
    blanks = [
        # '当我们来到乡村，见到“鸡犬相闻”的景象，会联想到陶渊明在《归园田居》中“_________，鸡鸣桑树颠”来表达对田园生活的赞美。',
        # '《蜀相》中，诗人运用带有咏叹情调的自问自答句式，把一种追思缅想情意，作了极为深微的表达并奠定了全诗“沈挚悲壮”的的句子是：____________，___________。',
        # '“白日依山尽，黄河入海流。______，_______。”',
        # "《赤壁赋》用 “_________，________”，写出月亮令人不易觉察的缓慢移动，逼真传神。",
        "元代戏剧家马致远的杂剧《青衫泪》根据白居易的诗《琵琶行》改编而成，剧名来自诗中的“_________，________”两句。"
    ]
    for blank in blanks:
        print(poem_retrieval(blank))
