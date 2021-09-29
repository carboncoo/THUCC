import streamlit as st
from thucc.engine.api import api_microwrite

def prompt_wbr(inputs):
    return inputs + '@@'

def app():

    st.title("微写作系统")

    with st.container():
        # 综合性微写作
        init_inputs_general = "健康是指一个人在身体、精神和社会等方面都处于良好的状态。"
        init_outputs_general = "健康是指一个人在身体、精神和社会等方面都处于良好的状态。也就是说，一个人的健康状况可以概括为：心理健康、精力充沛、智力正常、行为正常等四个方面。因此，当人在某方面出现了问题时，我们一定要重视和关注它，并把它看作是一种必然性的东西，不能掉以轻心，否则就会给自己带来不必要的麻烦，影响健康长寿。"

        st.write("## 自由写作")
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