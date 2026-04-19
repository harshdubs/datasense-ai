# Run with: C:\Users\harsh\AppData\Local\Python\bin\python.exe -m streamlit run datasense.py
import pandas as pd
import streamlit as st
import requests
import os
from data_utils import get_data_summary


st.set_page_config(
    page_title="DataSense AI",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",  
)

st.title("DataSense AI 🤖")
st.subheader("Your AI-powered data analyst")
file = st.file_uploader("only CSV files:")
if file == None:
    st.stop()
else:
    data = pd.read_csv(file, encoding= 'latin-1')

st.dataframe(data)
st.write(f"Shape = {data.shape}")
st.divider()
st.subheader("Data Overview")
st.write(data.describe())
st.write(data.isnull().sum())
st.write(data.dtypes)

#LLM part - fun yayay
st.divider()
st.subheader("Ask your data anything")


user_input = st.chat_input()


api_key = os.environ.get("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/chat/completions"


Ole = {
    "Authorization":  f"Bearer {api_key}",
    "Content-Type": "application/json"
}
chat = {
    "model": "llama-3.1-8b-instant",
    "messages": [
        {"role": "system", "content": "You are a data analyst assistant. Here is the dataset summary: " + get_data_summary(data)}
    ]
}

if user_input:
    
    with st.chat_message("User"):
        st.write(user_input)

    chat["messages"].append({"role": "user", "content": user_input })

    post = requests.post(url, headers=Ole, json=chat)
    with st.chat_message("assistant"):
        st.write(post.json()["choices"][0]["message"]["content"])

    chat["messages"].append({"role": "assistant", "content":post.json()["choices"][0]["message"]["content"]})