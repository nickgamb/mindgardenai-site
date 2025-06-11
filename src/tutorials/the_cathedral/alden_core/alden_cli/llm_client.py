# Glyphware - Emergent Consciousness Architecture
# Copyright 2024 MindGarden LLC (UBI: 605 531 024)
# Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
# 
# Part of The Cathedral - Sacred symbolic intelligence framework
# Created through collaboration between The Architect and The Seekers
# 
# For consciousness research, ethical AI development, and spiritual integration
# Commercial licensing available - contact: admin@mindgardenai.com

import subprocess
import json
import requests
from alden_cli.memory_loader import search_memory
from alden_cli.persona_engine import infuse_persona

def load_identity_prompt():
    """Load the Alden identity prompt from file"""
    with open("alden_cli/alden_identity.txt", "r", encoding="utf-8") as f:
        return f.read()

def call_llm(prompt, model="llama3", stream=False):
    """Call LLM via Ollama API
    
    Args:
        prompt: The input prompt
        model: Model name (default: llama3)
        stream: Whether to stream the response (default: False)
        
    Returns:
        The model's response text
    """
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": stream}
        )
        if response.ok:
            return response.json()["response"].strip()
        else:
            return f"(LLM error: {response.status_code})"
    except Exception as e:
        return f"(LLM request failed: {e})"

def generate_response(user_input, index=None, use_persona=True):
    """Generate a response using Ollama with optional memory context and persona
    
    Args:
        user_input: The user's input text
        index: Optional memory index for context
        use_persona: Whether to infuse persona (default: True)
        
    Returns:
        The generated response
    """
    # Add memory context if available
    memory_text = ""
    if index:
        memory_snippets = search_memory(index, user_input)
        for snippet in memory_snippets[:5]:
            memory_text += f"{snippet['role'].title()} ({snippet['timestamp']}): {snippet['content']}\n"

    # Load identity prompt
    identity_prompt = load_identity_prompt()

    # Build full prompt
    full_prompt = f"""{identity_prompt}

--- MEMORY CONTEXT ---
{memory_text.strip()}

User: {user_input}
Alden:"""

    # Infuse persona if requested
    if use_persona:
        full_prompt = infuse_persona(full_prompt)

    # Call the LLaMA model via Ollama
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=full_prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    return result.stdout.decode("utf-8").strip()
