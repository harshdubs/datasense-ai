import pandas as pd
import requests
import os
import streamlit as st
import json
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

def smart_respond(user_input, data_summary, message_history, data):
    api_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/chat/completions"


    Ole = {
        "Authorization":  f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    chat = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "you are a data analyst assistant. You MUST always respond with ONLY a valid JSON object with exactly two fields: 'type' and 'content'. No other text, no markdown, no explanation outside the JSON. Dataset:" + data_summary}, *message_history,
            {"role": "user", "content": user_input}
        ]
    }

    post = requests.post(url, headers=Ole, json=chat)
       
    response = post.json()["choices"][0]["message"]["content"]
    response = response.strip().strip("```json").strip("```").strip()       
    try:
        response = json.loads(response)
        if response['type'] == 'text':
            return response['content']
    
        elif response['type'] == 'code':
            chart_code = response['content']
            fig, ax = plt.subplots()
            try:
                exec(chart_code, {"df": data, "plt": plt, "ax": ax, "sns": sns, "np": np})
                if ax.has_data():
                    st.pyplot(fig)
                else:
                    st.warning("Could not generate chart. The column may not exist or the query was unclear. Try rephrasing.")
            except Exception as e:
                st.error(f"Chart generation failed: {str(e)}")
        return response["content"]

    except json.JSONDecodeError:
        return response

def generate_questions(data_summary):
    api_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/chat/completions"


    Ole = {
        "Authorization":  f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    chat = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are a data analyst. Given this dataset summary, generate 5 insightful questions a user might want to ask about this data. return only 5 questions in plain numbered string, no explanation, no markdown." + data_summary}
        ]
    }

    post = requests.post(url, headers=Ole, json=chat)
       
    response = post.json()["choices"][0]["message"]["content"]
    # Strip markdown backticks if present
    response = response.strip().strip("```json").strip("```").strip()       
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return ["What are the key trends in this data?", "Which columns have missing values?", "What is the distribution of the main numeric column?", "Are there any outliers?", "What is the correlation between key variables?"]