# app.py

import streamlit as st
from utils.dsar_generator import generate_dsar
from utils.audit_analyzer import analyze_policy
from utils.qna_answer import ask_privacy_question
import pdfplumber
import re
from markdown import markdown

st.set_page_config(page_title="PrivAI - PrivacyOps Assistant", layout="wide")

st.title("🛡️ PrivAI - AI PrivacyOps Assistant")
st.markdown("Empower users with AI-driven privacy tools: analyze policies, generate DSARs, and answer compliance questions.")

tab1, tab2, tab3 = st.tabs(["📄 Policy Analyzer", "📬 DSAR Generator", "💬 Privacy Q&A"])

# ------------------- TAB 1: Policy Analyzer -------------------
with tab1:
    st.subheader("🔍 Analyze Privacy Policy for GDPR/CCPA/DPDPA Compliance")

    uploaded_file = st.file_uploader("Upload a privacy policy PDF", type="pdf")

    if uploaded_file:
        with pdfplumber.open(uploaded_file) as pdf:
            policy_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

        if st.button("Analyze Policy", use_container_width=True):
            with st.spinner("Analyzing..."):
                result = analyze_policy(policy_text)

                st.success("✅ Analysis Complete")
                st.markdown("**📝 Compliance Summary:**")

                # Clean and format Markdown output
                cleaned_result = result.strip()
                cleaned_result = re.sub(r"```(.*?)```", r"\1", cleaned_result, flags=re.DOTALL)

                try:
                    st.markdown(cleaned_result, unsafe_allow_html=True)
                except Exception:
                    st.text(cleaned_result)

# ------------------- TAB 2: DSAR Generator -------------------
with tab2:
    st.subheader("✉️ Generate a DSAR (Data Subject Access Request)")

    with st.form("dsar_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        provider = st.text_input("Data Controller / Company Name")
        req_type = st.selectbox("Request Type", ["Access", "Deletion", "Correction", "Portability"])
        submitted = st.form_submit_button("Generate Letter")

    if submitted and name and email and provider and req_type:
        with st.spinner("Generating DSAR Letter..."):
            letter = generate_dsar(name, email, provider, req_type)
            st.success("✅ Letter Generated")
            st.text_area("DSAR Letter", letter, height=300)
    elif submitted:
        st.warning("⚠️ Please fill in all the fields.")

# ------------------- TAB 3: Privacy Q&A -------------------
with tab3:
    st.subheader("💬 Ask a Privacy Compliance Question (GDPR, CCPA, DPDPA etc.)")

    question = st.text_area("What do you want to know about privacy laws or data rights?")

    if st.button("Ask AI", use_container_width=True):
        if question.strip():
            with st.spinner("Thinking..."):
                answer = ask_privacy_question(question)
                st.success("✅ Answer")
                st.markdown("**🧠 Response:**")
                st.markdown(answer, unsafe_allow_html=True)
        else:
            st.warning("Please enter a valid question.")
