import streamlit as st
from thucc.engine.api import api_poem_retrieval

def app():

    st.title("中国古诗词检索系统")

    init_inputs = "当我们来到乡村，见到“鸡犬相闻”的景象，会联想到陶渊明在《归园田居》中“_________，鸡鸣桑树颠”来表达对田园生活的赞美。"
    init_outputs = "当我们来到乡村，见到“鸡犬相闻”的景象，会联想到陶渊明在《归园田居》中“**狗吠深巷中**，鸡鸣桑树颠”来表达对田园生活的赞美。"

    st.write("### 系统输入")
    inputs = st.text_area("", init_inputs)
    display = init_outputs
    if st.button('提交'):
        display = api_poem_retrieval(inputs)
        if not display:
            display = '未检索到相关诗词'

    st.write("### 检索结果")
    
    st.write(display)