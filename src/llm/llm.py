# src/llm.py

from openai import OpenAI
from src.config import Config

cfg = Config()
client = OpenAI(api_key=cfg.api_key)

def generate_sql(system_prompt: str, user_prompt: str, model="gpt-4.1-mini") -> str:
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )
    return response.output_text.strip()
