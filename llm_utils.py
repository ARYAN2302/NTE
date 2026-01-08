import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GOOGLE_API_KEY")
if not key:
    raise RuntimeError("Missing GOOGLE_API_KEY in .env")

client = genai.Client(api_key=key)
MODEL = "gemini-3-flash-preview"

def parse_json(text):
    text = str(text).strip()
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find('{'), text.rfind('}')
        if start != -1 and end != -1:
            return json.loads(text[start:end+1])
        raise

def call_llm(system, prompt, temp=0.7, tokens=2000, json_mode=False):
    config = {
        "temperature": temp,
        "max_output_tokens": tokens,
        "system_instruction": system,
    }
    
    if json_mode:
        config["response_mime_type"] = "application/json"

    try:
        res = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(**config)
        )
        return res.text
    except Exception as e:
        print(f"LLM Error: {e}")
        raise
