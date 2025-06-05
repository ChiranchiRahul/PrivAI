# app.py

import streamlit as st
from utils.dsar_generator import generate_dsar
from utils.audit_analyzer import analyze_policy
import pdfplumber
import os

st.set_page_config(page_title="PrivAI - PrivacyOps Assistant")

st.title("🛡️ PrivAI: PrivacyOps Assistant")

tabs = st.tabs(["📄 Privacy Policy Analyzer", "📬 Generate DSAR"])

with tabs[0]:
    st.subheader("Upload a Privacy Policy PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file:
        with pdfplumber.open(uploaded_file) as pdf:
            policy_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

        if st.button("Analyze Policy"):
            with st.spinner("Analyzing..."):
                report = analyze_policy(policy_text)
                st.success("Analysis Complete")
                st.text_area("Compliance Summary", report, height=300)

with tabs[1]:
    st.subheader("Generate a DSAR (Data Subject Access Request)")
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    provider = st.text_input("Data Controller / Company Name")
    req_type = st.selectbox("Request Type", ["Access", "Deletion", "Correction", "Portability"])

    if st.button("Generate DSAR Letter"):
        if name and email and provider and req_type:
            with st.spinner("Generating..."):
                dsar_text = generate_dsar(name, email, provider, req_type)
                st.text_area("DSAR Letter", dsar_text, height=300)
        else:
            st.warning("Please fill in all fields.")
