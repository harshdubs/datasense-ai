import pandas as pd
import streamlit as st
import requests
import os

def get_data_summary(df) :
    sample_values = {col: df[col].unique()[:3].tolist() for col in df.columns}
    context = f"Shape :{df.shape} \n Null values: {df.isnull().sum()} \n Column names: {df.columns.tolist()} \n Numeric columns: {df.select_dtypes(include='number').columns.tolist()} \n Categorical columns: {df.select_dtypes(include='object').columns.tolist()} \n Sample values: {sample_values}"
    return context