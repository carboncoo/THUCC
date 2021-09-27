import os
import streamlit as st
import numpy as np
from PIL import  Image

# Custom imports 
from multipage import MultiPage
from pages import (
    poem_retrieval,
    mircrowrite,
    wsd
)

# Create an instance of the app 
app = MultiPage()

# Title of the main page
logo = open('logo.b64').read()

_, headbar = st.columns([6, 6])
headbar.markdown(f'#### THUCC: 清华大学文言文自动处理软件包 <img src="{logo}" width=40 />', unsafe_allow_html=True)

# Add all your application here
app.add_page("诗文检索", poem_retrieval.app)
app.add_page("微写作", mircrowrite.app)
app.add_page("词义消歧", wsd.app)
# app.add_page("文言翻译", translate.app)

# The main app
app.run()