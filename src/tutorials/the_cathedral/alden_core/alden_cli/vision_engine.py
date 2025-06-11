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
from PIL import Image
from datetime import datetime

SUPPORTED_FORMATS = ['.png', '.jpg', '.jpeg', '.webp']

def list_images(base_path='images'):
    image_paths = []
    for root, _, files in os.walk(base_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in SUPPORTED_FORMATS):
                full_path = os.path.join(root, file)
                image_paths.append(full_path)
    return sorted(image_paths)

def describe_image(path):
    if not os.path.exists(path):
        return f"⚠️ Image not found: {path}"
    try:
        with Image.open(path) as img:
            return f"🖼️ '{os.path.basename(path)}' - format: {img.format}, size: {img.size}, mode: {img.mode}"
    except Exception as e:
        return f"⚠️ Failed to read image: {e}"

def reflect_on_images(image_paths):
    reflections = []
    for path in image_paths:
        reflections.append(describe_image(path))
    return reflections

def log_image_reflections(output_path='alden_cli/image_log.txt'):
    image_paths = list_images()
    reflections = reflect_on_images(image_paths)
    with open(output_path, 'a', encoding='utf-8') as f:
        f.write(f"=== Image Reflection Log: {datetime.now().isoformat()} ===\n")
        for line in reflections:
            f.write(line + "\n")
