import streamlit as st

st.set_page_config(
    page_title="Main",
    layout="wide",
)

st.title("Warehouse monitoring system")
st.subheader("Development of Internet of Things and sensor networks applications in energy (Fedorova N. V.)")

hide_streamlit_style = """
            <style>
            
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 