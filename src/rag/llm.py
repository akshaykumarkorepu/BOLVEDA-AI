import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def get_groq_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))


def stream_response(prompt):
    client = get_groq_client()

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
        stream=True,
    )

    for chunk in response:
        delta = chunk.choices[0].delta

        if hasattr(delta, "content") and delta.content is not None:
            yield delta.content
