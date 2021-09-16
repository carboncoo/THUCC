import json
import requests

def test_translate(srcList):
    url = "http://127.0.0.1:36789/translate/"
    ret = requests.post(url, json=srcList)
    return json.loads(ret.text)

if __name__ == '__main__':
    srcList = [
        "使吴越，致命讫即还",
        "吾终拒之，是近名也",
        "邀煜入宫治装",
        "上觉，遽诘所以",
        "煜之君臣，卒赖保全。"
    ]
    tgtList = test_translate(srcList)
    print(tgtList)