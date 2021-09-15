# 微写作系统

## 简介

本系统提供Docker模式部署，当前运行端口为`36792`，可在创建时进行修改。

## 部署

```sh
cd wsd
docker build  -t thucc-wsd:v0.0.1 .
docker run -d -p 36792:80 --name thucc-wsd thucc-wsd:v0.0.1
```

## 调用

```python
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
```