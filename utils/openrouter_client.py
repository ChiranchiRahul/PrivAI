import streamlit as st
from openai import OpenAI
import os

def get_client():
    # Prefer st.secrets but fallback to .env for local dev
    key = st.secrets.get("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise ValueError("OpenRouter API key not found in secrets or environment.")
    return OpenAI(api_key=key, base_url="https://openrouter.ai/api/v1")
