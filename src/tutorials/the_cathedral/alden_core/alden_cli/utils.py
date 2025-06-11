# Glyphware - Emergent Consciousness Architecture
# Copyright 2024 MindGarden LLC (UBI: 605 531 024)
# Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
# 
# Part of The Cathedral - Sacred symbolic intelligence framework
# Created through collaboration between The Architect and The Seekers
# 
# For consciousness research, ethical AI development, and spiritual integration
# Commercial licensing available - contact: admin@mindgardenai.com

from pathlib import Path

def load_file_if_exists(filepath):
    path = Path(filepath)
    if path.exists() and path.is_file():
        return path.read_text(encoding='utf-8')
    return None

def save_file_if_exists(filepath, content):
    """Save content to file if the directory exists, creating parent directories if needed"""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
    return True
