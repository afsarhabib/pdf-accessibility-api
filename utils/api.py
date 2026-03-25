import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://app:8000/api/v1/dashboard")

@st.cache_data(ttl=30)
def fetch_report():
    try:
        res = requests.get(API_URL, timeout=5)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return {"error": str(e)}