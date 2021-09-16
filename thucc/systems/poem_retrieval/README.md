# 诗歌检索系统

## 简介

本系统提供Docker模式部署，当前运行端口为`36793`，可在创建时进行修改。

## 部署

```sh
cd poem_retrieval
docker build  -t thucc-poemretrieval:v0.0.1 .
docker run -d -p 36793:80 --name thucc-poemretrieval thucc-poemretrieval:v0.0.1
```

## 调用

```python
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
```