import pdfplumber
from openai import OpenAI

client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

def analyze_privacy_policy(text):
    prompt = f"""
You are a privacy compliance auditor. Review this privacy policy and return a bullet-point list of risks, missing GDPR/CCPA clauses, and vague or non-compliant sections.

--- POLICY START ---
{text}
--- POLICY END ---
    """

    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
