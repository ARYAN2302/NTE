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
    except json.JSONDecodeError as e:
        # Try to find the JSON object if there's extra text
        start, end = text.find('{'), text.rfind('}')
        if start != -1 and end != -1:
            try:
                return json.loads(text[start:end+1])
            except json.JSONDecodeError:
                pass
        
        # Fix missing commas between elements in lists/objects
        import re
        repaired = text
        # Look for things like: "key": "value"\n    "next_key"
        # Only add a comma if the next character is a starting delimiter (", {, [) 
        # but NOT an ending delimiter (}, ])
        repaired = re.sub(r'("(?:\\["\\\/bfnrt]|[^\\"])*")\s*\n\s*(?=[{\["])', r'\1,\n', repaired)
        repaired = re.sub(r'([0-9]|true|false|null)\s*\n\s*(?=[{\["])', r'\1,\n', repaired)
        repaired = re.sub(r'(})\s*\n\s*(?=[{\["])', r'\1,\n', repaired)
        repaired = re.sub(r'(])\s*\n\s*(?=[{\["])', r'\1,\n', repaired)
        
        try:
            return json.loads(repaired)
        except:
            raise e

def call_llm(system, prompt, temp=0.7, tokens=4096, json_mode=False):
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
