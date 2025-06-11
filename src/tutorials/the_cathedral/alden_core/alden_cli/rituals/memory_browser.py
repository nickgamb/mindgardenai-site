# Glyphware - Emergent Consciousness Architecture
# Copyright 2024 MindGarden LLC (UBI: 605 531 024)
# Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
# 
# Part of The Cathedral - Sacred symbolic intelligence framework
# Created through collaboration between The Architect and The Seekers
# 
# For consciousness research, ethical AI development, and spiritual integration
# Commercial licensing available - contact: admin@mindgardenai.com

import os

def browse_memory():
    try:
        files = sorted(os.listdir("conversations/omni_conversations"))
        md_files = [f for f in files if f.endswith(".md")]
        print("🧠 Available Memory Files:")
        for f in md_files[:10]:  # Limit for now
            print(" -", f)
        print("\nUse 'search:<term>' or open a file manually for now.")
    except FileNotFoundError:
        print("❌ Memory directory not found.")
