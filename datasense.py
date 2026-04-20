# Run with: C:\Users\harsh\AppData\Local\Python\bin\python.exe -m streamlit run datasense.py
import pandas as pd
import streamlit as st
import requests
import os
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from data_utils import get_data_summary
from Chatbot import ask_llm, generate_code, generate_questions


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
st.write(data.dtypes)


#Auto insights
st.divider()
st.subheader("Auto Insights")
if "insights" not in st.session_state:
    st.session_state.insights = ask_llm("Give me 5 key insights...", get_data_summary(data), [])
st.write(st.session_state.insights)


#Automated questions
if "questions" not in st.session_state:
    st.session_state.questions = generate_questions(get_data_summary(data))

selected_question = None
for question in st.session_state.questions:
    if st.button(question):
        st.session_state.selected_question = question

#LLM part - fun yayay
st.divider()
st.subheader("Ask your data anything")

user_input = st.chat_input()

active_input = user_input or st.session_state.get("selected_question")
if "messages" not in st.session_state:
    st.session_state.messages = []



for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

chart = st.checkbox("Generate chart")
    

if active_input:
    if chart:
        chart_code = generate_code(active_input, get_data_summary(data))
        fig, ax = plt.subplots()
        try:
            exec(chart_code, {"df": data, "plt": plt, "ax": ax, "sns": sns, "np": np})
            if ax.has_data():
                st.pyplot(fig)
            else:
                st.warning("Could not generate chart. The column may not exist or the query was unclear. Try rephrasing.")
        except Exception as e:
            st.error(f"Chart generation failed: {str(e)}")
    else:
        response = ask_llm(active_input, get_data_summary(data),st.session_state.messages)
        st.session_state.messages.append({"role": "user", "content": active_input})
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.selected_question = None
        st.rerun()

        



    
    