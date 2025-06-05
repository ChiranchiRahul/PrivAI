# utils/audit_analyzer.py

from utils.openrouter_client import get_client

def analyze_policy(policy_text):
    client = get_client()

    messages = [
        {"role": "system", "content": "You are a privacy compliance auditor."},
        {"role": "user", "content": f"Analyze this privacy policy for GDPR/CCPA compliance:\n\n{policy_text}"}
    ]

    response = client.chat.completions.create(
        model="openrouter/openai/gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content.strip()
