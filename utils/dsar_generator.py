def generate_dsar(name, email, provider, req_type, client):
    prompt = f"""
    Write a formal DSAR letter based on the following info:
    Name: {name}
    Email: {email}
    Company: {provider}
    Request Type: {req_type}

    Make it polite, legally sound, and professional.
    """

    response = client.chat.completions.create(
        model="openrouter/openai/gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
