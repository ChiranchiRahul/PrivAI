# utils/dsar_generator.py

from utils.openrouter_client import get_client

def generate_dsar(name, email, provider, req_type):
    client = get_client()

    messages = [
        {"role": "system", "content": "You are a legal assistant generating DSAR letters."},
        {"role": "user", "content": f"Generate a Data Subject Access Request letter for {name}, email {email}, to {provider}, requesting {req_type}."}
    ]

    response = client.chat.completions.create(
        model="openrouter/openai/gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content.strip()
