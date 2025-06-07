# utils/qna_answer.py

from utils.openrouter_client import get_client
from utils.dpdpa_loader import load_dpdpa_chunks
from utils.gdpr_loader import load_gdpr_chunks
from utils.ccpa_loader import load_ccpa_chunks

DPDPA_CHUNKS = load_dpdpa_chunks()
GDPR_CHUNKS = load_gdpr_chunks()
CCPA_CHUNKS = load_ccpa_chunks()


def ask_privacy_question(question):
    client = get_client()

    include_dpdpa = any(x in question.lower() for x in ["dpdpa", "india", "Digital Personal Data Protection Act"])
    include_gdpr = any(x in question.lower() for x in ["gdpr", "europe", "eu","General Data Protection Regulation"])
    include_ccpa = any(x in question.lower() for x in ["ccpa", "california","California Consumer Privacy Act"])

    system_msg = (
    "You are a privacy assistant specialized in GDPR (EU), CCPA (California), and DPDPA (India). "
    "Base all answers strictly on actual provisions from the official text of each regulation. "
    "Do not invent or infer rights or obligations unless directly mentioned in the law."
)

    law_context = ""
    if include_gdpr:
        law_context += f"\n\n**GDPR Reference:**\n{GDPR_CHUNKS[0]}"
    if include_ccpa:
        law_context += f"\n\n**CCPA Reference:**\n{CCPA_CHUNKS[0]}"
    if include_dpdpa:
        law_context += f"\n\n**DPDPA Reference:**\n{DPDPA_CHUNKS[0]}"

    user_prompt = f"""
{law_context}

Now answer this question:
{question}
""" if law_context else question

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_prompt}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content.strip()
