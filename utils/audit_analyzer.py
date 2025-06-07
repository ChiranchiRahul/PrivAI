# utils/audit_analyzer.py

from utils.openrouter_client import get_client

def analyze_policy(policy_text):
    client = get_client()

    messages = [
        {
            "role": "system",
            "content": "You are a data privacy compliance expert."
        },
        {
            "role": "user",
            "content": f"Analyze the following privacy policy for compliance with GDPR (EU), CCPA (California), and DPDPA (India). Point out strengths, missing elements, and suggest improvements:\n\n{policy_text}"
        }
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content.strip()
