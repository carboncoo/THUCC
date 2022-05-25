# 微写作系统

## 简介

本系统提供Docker模式部署，当前运行端口为`36794`，可在创建时进行修改。

## 部署

<!-- ```sh
cd dictation
docker build  -t thucc-dictation:v0.0.1 .
docker run -d --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=8 -p 36794:80 --name thucc-dictation thucc-dictation:v0.0.1
``` -->

<!-- ```sh
cd dictation
docker build  -t thucc-dictation:v0.0.2 .
docker run -d -p 36794:80 --name thucc-dictation thucc-dictation:v0.0.2
``` -->

## 调用

```python
import json
import requests

def dictation(prompts):
    """
    Inputs: 
        prompts: [
            "毕业典礼上，校长引用《游褒禅山记》中的“________，________”两句，勉励学生在成长路上竭诚尽志，努力拼搏，做到无怨无悔。 $$",
            "学习中离不开积累。如果想表达积累对于结果的重要意义，我们可以引用的古诗文名句有：“________，________。” $$",
            "《子路、曾皙、冉有、公西华侍坐》中冉有认为自己能治理小国，使百姓富足，但他又用“________，________”表明自己还不能以礼乐教化百姓。 $$",
            "陶渊明身在宦海，心系田园，因此他在《归园田居》中运用比喻、对偶手法，写出了“________，________”的诗句。 $$",
        ]
    
    Outputs:
        generates: [
            "而世之奇伟、瑰怪、非常之观 常在于险远",
            "青青子衿 悠悠我心",
            "为国以礼 其言不让",
            "羁鸟恋旧林 池鱼思故渊"
        ]
    """
    url = "http://127.0.0.1:36794/dictation"
    ret = requests.post(url, json={'prompts': prompts})
    return json.loads(ret.text)
```