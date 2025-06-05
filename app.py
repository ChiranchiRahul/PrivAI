import streamlit as st
from openai import OpenAI
from utils.dsar_generator import generate_dsar
from utils.audit_generator import audit_privacy_policy

# 🔐 Use API key from secrets.toml
client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)

st.set_page_config(page_title="PrivAI – GenAI PrivacyOps Assistant", layout="centered")

# Sidebar Navigation
st.sidebar.title("🛠 Choose a Tool")
tool = st.sidebar.radio("", ["DSAR Generator", "Privacy Risk Audit"])

st.title("🔐 PrivAI – GenAI PrivacyOps Assistant")

if tool == "DSAR Generator":
    st.header("📮 DSAR Letter Generator")
    with st.form("dsar_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        provider = st.text_input("Company (e.g., Facebook)")
        req_type = st.selectbox("Request Type", ["Access", "Deletion"])
        submit = st.form_submit_button("Generate DSAR")

        if submit:
            dsar_text = generate_dsar(name, email, provider, req_type, client)
            st.subheader("✉️ Generated DSAR Letter")
            st.code(dsar_text)

elif tool == "Privacy Risk Audit":
    st.header("🕵️ Privacy Policy Risk Analyzer")
    uploaded_file = st.file_uploader("Upload a Privacy Policy PDF", type=["pdf"])
    if uploaded_file:
        import pdfplumber
        with pdfplumber.open(uploaded_file) as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        st.success("✅ File loaded. Running analysis...")

        with st.spinner("Auditing privacy policy..."):
            audit = audit_privacy_policy(text, client)
            st.markdown("### 📋 Risk Audit Report")
            st.markdown(audit)
