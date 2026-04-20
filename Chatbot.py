import pandas as pd
import requests
import os
import streamlit as st


def ask_llm(user_input, data_summary, message_history):
    api_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/chat/completions"


    Ole = {
        "Authorization":  f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    chat = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are a data analyst assistant. Here is the dataset summary: " + data_summary}, *message_history,
            {"role": "user", "content": user_input}
        ]
    }

    post = requests.post(url, headers=Ole, json=chat)
       
    response = post.json()["choices"][0]["message"]["content"]
    return response

def generate_code(user_input, data_summary):
    api_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/chat/completions"


    Ole = {
        "Authorization":  f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    chat = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are a Python code generator. Return only executable Python code with no explanation, no markdown, no backticks. Use `df` as the dataframe variable, `ax` for plotting, and `plt` for matplotlib. Always plot directly on `ax` using ax.hist(), ax.plot(), sns.histplot(ax=ax) etc. Never create a new figure inside the code." + data_summary},
            {"role": "user", "content": user_input}
        ]
    }
    post = requests.post(url, headers=Ole, json=chat)
       
    response = post.json()["choices"][0]["message"]["content"]
    return response