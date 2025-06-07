# utils/qna_answer.py

from utils.openrouter_client import get_client

def ask_privacy_question(question):
    client = get_client()

    messages = [
        {
            "role": "system",
            "content": "You are a privacy law assistant who answers questions based on GDPR (EU), CCPA (California), and DPDPA (India). Provide accurate, plain-language answers."
        },
        {
            "role": "user",
            "content": question
        }
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content.strip()
