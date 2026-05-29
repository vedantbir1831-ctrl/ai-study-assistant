import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_notes(text):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize these notes:\n{text}"
            }
        ]
    )
    return response.choices[0].message.content


def generate_quiz(text):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": f"Generate 5 MCQs from:\n{text}"
            }
        ]
    )
    return response.choices[0].message.content