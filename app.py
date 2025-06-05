# app.py

import streamlit as st
from utils.dsar_generator import generate_dsar
from utils.audit_analyzer import analyze_policy
from utils.qna_answer import ask_privacy_question  # ← NEW MODULE
import pdfplumber

st.set_page_config(page_title="PrivAI - PrivacyOps Assistant", layout="wide")

st.title("🛡️ PrivAI - AI PrivacyOps Assistant")
st.markdown("Empower your users with automated privacy tools: policy analysis, DSAR generation, and Q&A.")

tab1, tab2, tab3 = st.tabs(["📄 Policy Analyzer", "📬 DSAR Generator", "💬 Privacy Q&A"])

# --- TAB 1: Policy Analyzer ---
with tab1:
    st.subheader("🔍 Analyze Privacy Policy for Compliance")

    uploaded_file = st.file_uploader("Upload your privacy policy (PDF format)", type="pdf")

    if uploaded_file:
        with pdfplumber.open(uploaded_file) as pdf:
            policy_text = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])

        if st.button("Analyze Policy", use_container_width=True):
            with st.spinner("Analyzing..."):
                result = analyze_policy(policy_text)
                st.success("✅ Analysis Complete")
                st.text_area("Compliance Summary", result, height=300)

# --- TAB 2: DSAR Generator ---
with tab2:
    st.subheader("✉️ Generate a DSAR (Data Subject Access Request) Letter")

    with st.form("dsar_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        provider = st.text_input("Data Controller / Company Name")
        req_type = st.selectbox("Request Type", ["Access", "Deletion", "Correction", "Portability"])
        submit = st.form_submit_button("Generate Letter")

    if submit and name and email and provider and req_type:
        with st.spinner("Generating DSAR..."):
            letter = generate_dsar(name, email, provider, req_type)
            st.success("✅ DSAR Letter Generated")
            st.text_area("Generated Letter", letter, height=300)
    elif submit:
        st.warning("Please fill all fields to generate the letter.")

# --- TAB 3: Privacy Q&A ---
with tab3:
    st.subheader("💬 Ask a Privacy Compliance Question")

    question = st.text_area("Ask about GDPR, CCPA, or data rights...")
    if st.button("Ask AI", use_container_width=True):
        if question.strip():
            with st.spinner("Thinking..."):
                answer = ask_privacy_question(question)
                st.success("✅ Answered")
                st.markdown(f"**🧠 Answer:**\n\n{answer}")
        else:
            st.warning("Please enter a question.")
