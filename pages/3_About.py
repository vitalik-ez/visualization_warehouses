import streamlit as st
from PIL import Image

st.set_page_config(page_title="About", layout="wide")
st.title("About")
image = Image.open('./images/team.jpg')

st.image(image, caption='Team')

hide_streamlit_style = """
            <style>
            
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
