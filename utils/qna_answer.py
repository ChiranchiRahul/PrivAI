from utils.openrouter_client import get_client

def ask_privacy_question(question):
    client = get_client()

    messages = [
        {"role": "system", "content": "You are a privacy and data protection expert."},
        {"role": "user", "content": question}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content.strip()
