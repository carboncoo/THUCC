import os
import streamlit as st
import numpy as np
from PIL import  Image

# Custom imports 
from multipage import MultiPage
from pages import (
    dictation,
    mircrowrite,
    translate
)

# Create an instance of the app 
app = MultiPage()

# Title of the main page
logo = open('logo.b64').read()

st.set_page_config(page_title='THUCC Demo', page_icon = logo, layout='centered', initial_sidebar_state = 'auto')

_, headbar = st.columns([6, 6])
headbar.markdown(f'#### THUCC: 清华大学文言文自动处理软件包 <img src="{logo}" width=40 />', unsafe_allow_html=True)

# Add all your application here
app.add_page("古诗文默写", dictation.app)
app.add_page("微写作", mircrowrite.app)
app.add_page("文言文翻译", translate.app)
# app.add_page("文言翻译", translate.app)

# The main app
app.run()