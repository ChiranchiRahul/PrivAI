# utils/audit_analyzer.py

from utils.openrouter_client import get_client
from utils.dpdpa_loader import load_dpdpa_chunks
from utils.gdpr_loader import load_gdpr_chunks
from utils.ccpa_loader import load_ccpa_chunks

# Load law chunks
DPDPA_CHUNKS = load_dpdpa_chunks()
GDPR_CHUNKS = load_gdpr_chunks()
CCPA_CHUNKS = load_ccpa_chunks()


def analyze_policy(policy_text):
    client = get_client()

    system_msg = """
    You are a privacy compliance expert skilled in GDPR (EU), CCPA (California), and DPDPA (India).
    Given a privacy policy and references from all three laws, assess compliance, highlight gaps, and suggest improvements.
    """

    user_prompt = f"""
Review the following privacy policy for compliance with:
- GDPR (EU)
- CCPA (California, USA)
- DPDPA (India)

Use the following grounded references:

**GDPR Excerpt:**
{GDPR_CHUNKS[0]}

**CCPA Excerpt:**
{CCPA_CHUNKS[0]}

**DPDPA Excerpt:**
{DPDPA_CHUNKS[0]}

Now, analyze this privacy policy:

{policy_text}

Provide a structured compliance audit for each regulation (GDPR, CCPA, DPDPA):
- ✅ Compliant Areas
- ❌ Missing Elements
- 💡 Suggestions to improve compliance
"""

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_prompt}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content.strip()
