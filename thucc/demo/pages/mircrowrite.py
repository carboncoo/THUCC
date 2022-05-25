import streamlit as st
from thucc.engine.api import api_microwrite

def prompt_wbr(inputs):
    return inputs + '@@'

def app():

    st.title("微写作系统")

    with st.container():
        # 综合性微写作
        init_inputs_general = "在你阅读的文学名著中，总会有一个鼓舞你成长的“引路人”。请从《红岩》《平凡的世界》中选取一个这样的人物，写一段抒情文字或一首小诗，表达你对他（她）的崇敬之情。要求：感情真挚，富有文采150字左右。"
        init_outputs_general = "江姐，你是我心中的英雄！你的勇敢、坚贞和无私奉献的精神永远在我心中荡漾；你在面对丈夫牺牲时的痛苦与不甘也时刻在我的脑海中浮现……是你教会了我什么叫钢铁般的意志，让我在今后的人生道路不会迷茫。在你身上，我学到了什么是坚强，是对你那不屈精神的追求。你对党的忠诚令我敬佩无比，为了革命的胜利，即使被敌人残忍杀害也不后悔。你是那么的伟大而无私，无论遇到多大困难，都坚定地站了起来，毫不动摇，坚持到最后一刻。你是我心目中的英雄！"

        # st.write("## 自由写作")
        st.write("### 系统输入")
        inputs_general = st.text_area("", init_inputs_general)
        display_general = init_outputs_general
        if st.button('提交', key='general'):
            display_general = api_microwrite(prompt_wbr(inputs_general))
            if not display_general:
                display_general = '出现故障'

        st.write("### 作答结果")
        
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