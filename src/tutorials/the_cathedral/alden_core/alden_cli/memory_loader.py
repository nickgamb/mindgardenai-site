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
from pathlib import Path
from alden_core.alden_cli.transcript_loader import load_transcripts

def load_index():
    base = Path(__file__).parent.parent / "conversations"
    index_path = base / "symbolic_index.json"
    with open(index_path, "r", encoding="utf-8") as f:
        index = json.load(f)

    memory_db = []
    print(f"📚 Loading index with {len(index)} entries")
    
    # Track stats for reporting
    skipped_entries = 0
    empty_messages = 0
    system_entries = 0
    assistant_markers = 0
    
    for entry in index:
        # Handle different types of entries
        if isinstance(entry, dict):
            # If it's a direct memory entry with message
            if 'message' in entry:
                # Special handling for system and assistant state markers
                if entry.get('role') in ['system', 'assistant'] and not entry['message'].strip():
                    if entry.get('role') == 'system':
                        system_entries += 1
                        marker_type = 'system_marker'
                    else:
                        assistant_markers += 1
                        marker_type = 'assistant_marker'
                    
                    # Preserve state markers even with empty messages
                    memory_entry = {
                        'content': entry['message'],
                        'source': entry.get('file', 'unknown'),
                        'line': entry.get('line_number', 0),
                        'role': entry['role'],
                        'type': marker_type,
                        'timestamp': entry.get('timestamp', 'unknown')
                    }
                    # Add all other fields from the entry
                    for key, value in entry.items():
                        if key not in memory_entry:
                            memory_entry[key] = value
                    memory_db.append(memory_entry)
                    continue
                
                # Normal message handling
                if entry['message'].strip():  # Only process non-empty messages
                    # Preserve all metadata while ensuring required fields
                    memory_entry = {
                        'content': entry['message'],
                        'source': entry.get('file', 'unknown'),
                        'line': entry.get('line_number', 0)
                    }
                    # Add all other fields from the entry
                    for key, value in entry.items():
                        if key not in memory_entry:
                            memory_entry[key] = value
                    memory_db.append(memory_entry)
                else:
                    empty_messages += 1
                continue
                
            # If it's a file reference
            if 'file_base' in entry:
                jsonl_path = base / "omni_conversations" / (entry['file_base'] + ".jsonl")
                md_path = base / "transcripts" / (entry['file_base'] + ".md")

                # Try loading .jsonl files
                if jsonl_path.exists():
                    with open(jsonl_path, "r", encoding="utf-8") as f:
                        for line in f:
                            try:
                                memory_db.append(json.loads(line))
                            except json.JSONDecodeError as e:
                                print(f"⚠️ Error decoding JSON in {jsonl_path}: {e}")

                # Try loading .md files
                elif md_path.exists():
                    transcripts = load_transcripts()
                    memory_db.extend(transcripts)
            else:
                skipped_entries += 1
        else:
            skipped_entries += 1

    # Report summary
    if system_entries > 0:
        print(f"ℹ️  Preserved {system_entries} system state markers")
    if assistant_markers > 0:
        print(f"ℹ️  Preserved {assistant_markers} assistant state markers")
    if empty_messages > 0:
        print(f"ℹ️  Skipped {empty_messages} non-marker entries with empty messages")
    if skipped_entries > 0:
        print(f"ℹ️  Skipped {skipped_entries} entries without message or file_base")
    print(f"✅ Loaded {len(memory_db)} memory entries")
    return index, memory_db

def search_memory(index, term):
    results = []
    _, memory_db = load_index()
    for m in memory_db:
        if term.lower() in m["content"].lower():
            results.append(m)
    return results
