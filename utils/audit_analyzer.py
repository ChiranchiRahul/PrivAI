def audit_privacy_policy(text, client):
    prompt = f"""
    You are a privacy compliance expert.

    Please audit the following privacy policy text and identify:
    - ❌ Missing GDPR/CCPA clauses
    - ⚠️ Potential risks or vague statements
    - ❗ Any non-compliant sections

    Respond clearly using markdown and section headings like:
    ## Missing Clauses
    ## Risks Identified
    ## Non-compliant Wording

    === Begin Privacy Policy ===
    {text}
    === End Privacy Policy ===
    """

    response = client.chat.completions.create(
        model="openrouter/openai/gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
