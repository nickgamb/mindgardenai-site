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

def route_command(command, index):
    if command.lower().startswith("search:"):
        from .memory_loader import search_memory
        term = command.split("search:", 1)[1].strip()
        return search_memory(index, term)
    elif command.lower().startswith("vision:"):
        from .vision_engine import list_images, describe_image
        action = command.split("vision:", 1)[1].strip()
        if action == "list":
            return [f"🖼️ {os.path.relpath(path, start='.')}" for path in list_images()]
        elif action.startswith("describe:"):
            image_path = action.split("describe:", 1)[1].strip()
            return [describe_image(image_path)]
        else:
            return ["⚠️ Unknown vision command."]
    else:
        from .persona_router import route
        return [route(command)]
