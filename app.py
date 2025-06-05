import streamlit as st
from openai import OpenAI

# OpenRouter client setup with GPT-3.5
client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

from utils.dsar_generator import generate_dsar
from utils.audit_analyzer import extract_text_from_pdf, analyze_privacy_policy

st.set_page_config(page_title="PrivAI – GenAI PrivacyOps", layout="centered")
st.title("🔐 PrivAI – GenAI PrivacyOps Assistant")

menu = st.sidebar.radio("🛠️ Choose a Tool", [
    "DSAR Generator",
    "Privacy Risk Audit",
    "Privacy Q&A"
])

if menu == "DSAR Generator":
    st.header("📬 DSAR Letter Generator")
    with st.form("dsar_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        provider = st.text_input("Company (e.g., Facebook)")
        req_type = st.selectbox("Request Type", ["Access", "Deletion"])
        submit = st.form_submit_button("Generate DSAR")
        if submit:
            dsar_text = generate_dsar(name, email, provider, req_type)
            st.subheader("✉️ Generated DSAR Letter")
            st.code(dsar_text)

elif menu == "Privacy Risk Audit":
    st.header("📄 Privacy Policy Risk Analyzer")
    file = st.file_uploader("Upload a Privacy Policy PDF", type="pdf")
    if file:
        with st.spinner("🔍 Analyzing..."):
            text = extract_text_from_pdf(file)
            if text:
                report = analyze_privacy_policy(text)
                st.subheader("🧾 Risk Audit Report")
                st.markdown(report)
            else:
                st.error("⚠️ No readable text found in the uploaded PDF.")

elif menu == "Privacy Q&A":
    st.header("💬 Ask a Privacy Law Question")
    query = st.text_input("Type your question (e.g., Do I need cookie consent in the EU?)")
    if query:
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="openai/gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a privacy law expert well-versed in GDPR, CCPA, and HIPAA."},
                    {"role": "user", "content": query}
                ]
            )
            st.subheader("🧠 Answer")
            st.markdown(response.choices[0].message.content)
