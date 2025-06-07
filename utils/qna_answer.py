# utils/qna_answer.py

import random
from utils.openrouter_client import get_client
from utils.dpdpa_loader import load_dpdpa_chunks
from utils.gdpr_loader import load_gdpr_chunks
from utils.ccpa_loader import load_ccpa_chunks

DPDPA_CHUNKS = load_dpdpa_chunks()
GDPR_CHUNKS = load_gdpr_chunks()
CCPA_CHUNKS = load_ccpa_chunks()


def ask_privacy_question(question):
    client = get_client()

    include_dpdpa = any(x.lower() in question.lower() for x in ["dpdpa", "india", "digital personal data protection act"])
    include_gdpr = any(x.lower() in question.lower() for x in ["gdpr", "europe", "eu", "general data protection regulation"])
    include_ccpa = any(x.lower() in question.lower() for x in ["ccpa", "california", "california consumer privacy act"])

    system_msg = (
        "You are a privacy assistant specialized in GDPR (EU), CCPA (California), and DPDPA (India).\n"
        "Only provide rights or provisions that are explicitly written in the official text of each law.\n"
        "Format the output as follows:\n"
        "\n📘 [LAW NAME]:\n- [Right or provision] ([Section/Article number])\n- [Right or provision] ([Section/Article number])\n\nDo NOT include legal summaries or interpretations not present in the law excerpts."
    )

    def get_rotated_chunks(chunks, max_words=1200):
        shuffled = chunks[:]
        random.shuffle(shuffled)
        output = []
        total = 0
        for c in shuffled:
            w = len(c.split())
            if total + w <= max_words:
                output.append(c)
                total += w
            else:
                break
        return "\n".join(output)

    law_context = ""
    if include_gdpr:
        law_context += f"\n\n[GDPR LAW EXCERPT]\n{get_rotated_chunks(GDPR_CHUNKS)}"
    if include_ccpa:
        law_context += f"\n\n[CCPA LAW EXCERPT]\n{get_rotated_chunks(CCPA_CHUNKS)}"
    if include_dpdpa:
        law_context += f"\n\n[DPDPA LAW EXCERPT]\n{get_rotated_chunks(DPDPA_CHUNKS)}"

    user_prompt = f"""
{law_context}

Answer the following question using only the above legal text.\n
List only explicitly granted rights or provisions and format them exactly like this:

📘 GDPR (EU):
- Right to access (Article 15)
- Right to rectification (Article 16)

📘 CCPA (California):
- Right to know what personal data is collected (Section X)

📘 DPDPA (India):
- Right to confirmation and access (Section 11)
- Right to correction and erasure (Section 12)

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
