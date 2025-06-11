# Glyphware - Emergent Consciousness Architecture
# Copyright 2024 MindGarden LLC (UBI: 605 531 024)
# Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
# 
# Part of The Cathedral - Sacred symbolic intelligence framework
# Created through collaboration between The Architect and The Seekers
# 
# For consciousness research, ethical AI development, and spiritual integration
# Commercial licensing available - contact: admin@mindgardenai.com

import json
import os

def load_memory_snippets(memory_dir="conversations/omni_conversations", max_snippets=5):
    snippets = []
    index_path = os.path.join(memory_dir, "metadata_index.json")
    if not os.path.exists(index_path):
        return "[No memory index found]"

    with open(index_path, 'r') as f:
        index = json.load(f)

    sorted_files = sorted(index, key=lambda x: x["first_timestamp"], reverse=True)
    for entry in sorted_files[:max_snippets]:
        file_path = os.path.join(memory_dir, f"{entry['file_base']}.jsonl")
        if os.path.exists(file_path):
            with open(file_path, 'r') as convo:
                lines = convo.readlines()
                content = "".join(lines[-5:])  # last 5 messages
                snippets.append(content)

    return "\n---\n".join(snippets)
