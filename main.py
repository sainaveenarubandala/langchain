import os
from constants import Openai_key
from langchain.llms import OpenAI
import streamlit as st
os.environ["OPENAI_API_KEY"] = Openai_key
st.title('langchain demo with open API')
input_text=st.text_input("Enter a port number (e.g., 22, 80, 443) or protocol (e.g., FTP, SSH)")

llm=OpenAI(temperature=0.8)



if input_text:
    st.write(llm(input_text))