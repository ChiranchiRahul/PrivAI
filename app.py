import os
import streamlit as st
from openai import OpenAI
from utils.dsar_generator import generate_dsar
from utils.audit_analyzer import audit_privacy_policy

# ✅ Load API key from environment variable or fallback hardcoded value
api_key = os.getenv("OPENROUTER_API_KEY", "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")
client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

# 🏠 Sidebar Navigation
st.sidebar.title("🔒 PrivAI: PrivacyOps Assistant")
page = st.sidebar.radio("Choose a Tool", ["DSAR Generator", "Privacy Risk Audit"])

# 📄 DSAR Generator
if page == "DSAR Generator":
    st.title("📄 DSAR Generator")
    with st.form("dsar_form"):
        name = st.text_input("Full Name", placeholder="Rahul Chiranchi")
        email = st.text_input("Email", placeholder="your@email.com")
        provider = st.text_input("Company Name", placeholder="Meta")
        req_type = st.selectbox("Request Type", ["Access", "Deletion"])
        submit = st.form_submit_button("Generate DSAR")
        if submit:
            dsar_text = generate_dsar(name, email, provider, req_type, client)
            st.subheader("✉️ Generated DSAR Letter")
            st.code(dsar_text)

# 🔎 Privacy Risk Analyzer
elif page == "Privacy Risk Audit":
    st.title("🔍 Privacy Policy Risk Audit")
    uploaded_file = st.file_uploader("Upload Privacy Policy (PDF)", type=["pdf"])
    if uploaded_file is not None:
        with st.spinner("Analyzing for risks..."):
            report = audit_privacy_policy(uploaded_file, client)
            st.success("✅ Audit Complete")
            st.subheader("🧾 Risk Audit Report")
            st.markdown(report)
