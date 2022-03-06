# 古诗理解选择系统

## 简介

本系统提供Docker模式部署，当前运行端口为`36796`，可在创建时进行修改。

## 部署

```sh
cd dictation
docker build  -t thucc-poemuselect:v0.0.1 .
docker run -d -p 36796:80 --name thucc-poemuselect thucc-poemuselect:v0.0.1
```

## 调用

```python
import json
import requests

def test_uselect(question):
    url = "http://127.0.0.1:36796/poem_uselect"
    ret = requests.post(url, json={'question': question})
    return json.loads(ret.text)

if __name__ == '__main__':
    question = {
        "question_id": "test01_13",
        "is_correct": True,
        "choices": ["梦中李白的到来离去，都令杜甫感到局促不安。", "“苦道来不易”写出了行路艰辛，二人见面不易。", "“冠盖满京华”，写出了李白在长安的交游之广。", "“千秋万岁名”，体现出杜甫对李白极高的评价。"],
        "title": "梦李白",
        "dynasty": "唐",
        "poet": "杜甫",
        "poem": "浮云终日行，游子久不至。三夜频梦君，情亲见君意。告归常局促，苦道来不易。江湖多风波，舟楫恐失坠。出门搔白首，若负平生志。冠盖满京华，斯人独憔悴。孰云网恢恢，将老身反累。千秋万岁名，寂寞身后事。"
    }
    result = test_uselect(question)
    print(result)
```