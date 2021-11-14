import streamlit as st
from thucc.engine.api import api_microwrite

def prompt_wbr(inputs):
    return inputs + '@@'

def app():

    st.title("微写作系统")

    with st.container():
        # 综合性微写作
        init_inputs_general = "班级要举行一次读书交流活动，请你在此次活动上向大家推介一本你最喜欢的书。要求：语言简明，条理清楚。"
        init_outputs_general = "《老人与海》这本书讲述了一个人出海的经过和最终取得胜利的故事，我非常推荐大家去阅读它。书中的圣地亚哥是一位硬汉形象，面对大马林鱼时他没有丝毫退缩，而是勇敢地与其搏斗。最后也取得了巨大的收获，我们也应该像这位英雄一样不屈服于现实。 "

        # st.write("## 自由写作")
        st.write("### 系统输入")
        inputs_general = st.text_area("", init_inputs_general)
        display_general = init_outputs_general
        if st.button('提交', key='general'):
            display_general = inputs_general + api_microwrite(inputs_general)
            if not display_general:
                display_general = '出现故障'

        st.write("### 系统输出")
        
        st.write(display_general)

    # st.write("----------------")

    # with st.container():
    #     # 整本书阅读
    #     init_inputs_wbr = "鲁迅先生评价《红楼梦》时谈到“至于说到《红楼梦》的价值，可是在中国底小说中实在是不可多得的。其要点在敢于如实描写，并无讳饰，和前的小说叙好人完全是好，坏人完全是坏的，大不相同，所以其中所叙的人物，都是真的人物。总之自有《红楼梦》出来以后，传统的思想和写法都打破了。”《红楼梦》塑造人物注重表现人物性格的复杂性及其发展变化，请从贾宝玉、林黛玉、薛宝钗、王熙凤中任选一个人物结合鲁迅先生的评价和作品内容简要阐明你对他（她）的理解。"
    #     init_outputs_wbr = ""

    #     st.write("## 整本书阅读")
    #     st.write("### 系统输入")
    #     inputs_wbr = st.text_area("", init_inputs_wbr, height=200)
    #     display_wbr = init_outputs_wbr
    #     if st.button('提交', key='wbr'):
    #         display_wbr = inputs_wbr + api_microwrite(prompt_wbr(inputs_wbr))
    #         if not display_wbr:
    #             display_wbr = '出现故障'

    #     st.write("### 系统输出")
        
    #     st.write(display_wbr)