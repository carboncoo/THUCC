# 翻译系统

## 简介

本系统提供Docker模式部署，默认端口为`36789`，可在`app.py`里进行修改

## 部署

```sh
cd translate
docker build  -t thucc-translate:v0.0.1 .
p
```

## 调用

```python
import json
import requests

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
    url = "http://127.0.0.1:36789/translate/"
    ret = requests.post(url, json=srcList)
    tgtList = json.loads(ret.text)
    return tgtList
```