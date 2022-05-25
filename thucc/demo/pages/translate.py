import streamlit as st
from thucc.engine.api import api_translate

def prompt_wbr(inputs):
    return inputs + '@@'

def app():

    st.title("文言文翻译系统")

    with st.container():
        # 文言文翻译
        init_inputs_general = "使吴越，致命讫即还\n上觉，遽诘所以"
        init_outputs_general = "出使吴越，到使命完成就立即还朝\n\n皇上发现了，立即问什么原因"

        # st.write("## 自由写作")
        st.write("### 系统输入")
        inputs_general = st.text_area("", init_inputs_general).split('\n')
        display_general = init_outputs_general
        if st.button('提交', key='general'):
            display_general = '\n\n'.join(api_translate(inputs_general))
            print(display_general)
            if not display_general:
                display_general = '出现故障'

        st.write("### 作答结果")
        
        st.write(display_general)