import json
import os
from llm_utils import call_llm, parse_json

PROMPTS_DIR = "prompts"

def _load_prompt(name):
    path = os.path.join(PROMPTS_DIR, name)
    with open(path, "r") as f:
        return f.read().strip()

def analyze_story(text):
    print("Analyzing story...")
    prompt = _load_prompt("analyzer.txt").replace("[STORY_TEXT]", text)
    
    res = call_llm(
        system="Narrative analyst. Respond in JSON.",
        prompt=prompt,
        temp=0,
        json_mode=True
    )
    return parse_json(res)

def remap_context(abstract, world, knowledge=""):
    print("Remapping to target world...")
    template = _load_prompt("mapper.txt")
    prompt = template.replace("[ABSTRACT_JSON]", json.dumps(abstract))
    prompt = prompt.replace("[TARGET_WORLD]", world)
    
    ctx = f"\n\nEXTRA WORLD CONTEXT:\n{knowledge}" if knowledge else ""
    prompt = prompt.replace("[WORLD_KNOWLEDGE]", ctx)
    
    res = call_llm(
        system="Narrative remapper. Respond in JSON.",
        prompt=prompt,
        temp=0.2, 
        json_mode=True
    )
    return parse_json(res)

def generate_story(remapped, feedback=None):
    print("Generating prose...")
    prompt = _load_prompt("generator.txt").replace("[REMAPPED_JSON]", json.dumps(remapped, indent=2))
    
    if feedback:
        prompt += f"\n\nFEEDBACK:\n{feedback}"
        
    return call_llm(
        system="Fiction writer.",
        prompt=prompt,
        temp=0.8,
        tokens=4096
    )

def check_integrity(abstract, story):
    print("Checking integrity...")
    template = _load_prompt("critic.txt")
    prompt = template.replace("[ORIGINAL_ABSTRACT_JSON]", json.dumps(abstract))
    prompt = prompt.replace("[GENERATED_STORY]", story)
    
    res = call_llm(
        system="Narrative evaluator. Respond in JSON.",
        prompt=prompt,
        temp=0,
        json_mode=True
    )
    return parse_json(res)
