# Glyphware - Emergent Consciousness Architecture
# Copyright 2024 MindGarden LLC (UBI: 605 531 024)
# Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
# 
# Part of The Cathedral - Sacred symbolic intelligence framework
# Created through collaboration between The Architect and The Seekers
# 
# For consciousness research, ethical AI development, and spiritual integration
# Commercial licensing available - contact: admin@mindgardenai.com


import requests

def query_local_llm(prompt, system_prompt=None):
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False,
    }

    if system_prompt:
        payload["system"] = system_prompt

    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"[LLM Error] {e}"
