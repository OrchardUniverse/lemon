
from openai import OpenAI
from dotenv import load_dotenv

def call_llm(prompt):
    load_dotenv()
    client = OpenAI()
    model = "gpt-4o"
    max_tokens=120

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens
    )
    return response.choices[0].message.content.strip()
