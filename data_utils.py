import pandas as pd
import streamlit as st
import requests
import os

def get_data_summary(df) :
    context = f"Shape :{df.shape} \n Columns and data types: {df.dtypes} \n Description: {df.describe()} \n Null values: {df.isnull().sum()}\n Head: {df.head()}"
    return context