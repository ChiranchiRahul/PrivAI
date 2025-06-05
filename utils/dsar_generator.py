from openai import OpenAI

client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

def generate_dsar(name, email, provider, request_type):
    prompt = f"""Draft a formal {request_type.upper()} request under GDPR for the following user:

    Name: {name}
    Email: {email}
    Company: {provider}

    Make it polite, legally sound, and professional."""

    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
