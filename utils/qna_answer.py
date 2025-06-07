from utils.openrouter_client import get_client
from utils.dpdpa_loader import load_dpdpa_chunks

# Load DPDPA text once when app starts
DPDPA_CHUNKS = load_dpdpa_chunks()

def ask_privacy_question(question):
    client = get_client()

    # Check if DPDPA is relevant
    include_dpdpa = any(x in question.lower() for x in ["dpdpa", "india", "Digital Personal Data Protection Act"])

    system_msg = (
        "You are a privacy assistant specialized in GDPR, CCPA, and DPDPA (India). "
        "Answer clearly using plain language."
    )

    if include_dpdpa:
        # Inject top 3 chunks from DPDPA (very simple for now)
        law_context = "\n\n".join(DPDPA_CHUNKS[:3])
        user_prompt = f"""
Refer to the following text from India's DPDPA:

{law_context}

Now answer this question:
{question}
"""
    else:
        user_prompt = question

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_prompt}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content.strip()
