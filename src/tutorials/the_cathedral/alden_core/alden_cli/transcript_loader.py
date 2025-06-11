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
import yaml

TRANSCRIPT_DIR = os.path.join(os.path.dirname(__file__), "..", "transcripts")

# Global reference to session log (will be set by main.py)
session_log_ref = None

def set_transcript_log_reference(log_ref):
    """Set reference to the main session log"""
    global session_log_ref
    session_log_ref = log_ref

def log_transcript_activity(content):
    """Log transcript activity to the session log if available"""
    if session_log_ref is not None:
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        session_log_ref.append({
            "timestamp": timestamp,
            "type": "transcript",
            "content": content
        })

def load_transcripts():
    transcripts = []
    if not os.path.exists(TRANSCRIPT_DIR):
        log_transcript_activity("Transcripts directory does not exist")
        print("⚠️ Transcripts directory does not exist.")
        return transcripts

    transcript_count = 0
    for filename in os.listdir(TRANSCRIPT_DIR):
        if filename.endswith(".md") and not filename.startswith("session_"):
            path = os.path.join(TRANSCRIPT_DIR, filename)
            try:
                with open(path, "r", encoding="utf-8") as file:
                    # Read the entire file content
                    content = file.read()
                    # Split the content into YAML front matter and the main content
                    if content.startswith("---"):
                        parts = content.split("---", 2)
                        if len(parts) >= 3:
                            yaml_content = parts[1]
                            main_content = parts[2]
                            # Parse the YAML front matter
                            metadata = yaml.safe_load(yaml_content)
                            transcripts.append({"filename": filename, "metadata": metadata, "content": main_content})
                        else:
                            print(f"⚠️ Invalid YAML front matter in {filename}.")
                            log_transcript_activity(f"Invalid YAML front matter in {filename}")
                    else:
                        # If no YAML front matter, treat the whole file as content
                        transcripts.append({"filename": filename, "content": content})
                    transcript_count += 1
            except Exception as e:
                error_msg = f"Error loading {filename}: {e}"
                print(f"⚠️ {error_msg}")
                log_transcript_activity(error_msg)
    
    # Filter out any non-dictionary items just in case
    transcripts = [t for t in transcripts if isinstance(t, dict) and "content" in t]
    if not transcripts:
        log_transcript_activity("No valid transcripts found")
        print(f"⚠️ No valid messages found in transcripts.")
    else:
        log_transcript_activity(f"Loaded {transcript_count} transcript files ({len(transcripts)} valid entries)")
    
    return transcripts

def get_transcript_echo(transcripts, keywords):
    """
    Search transcripts for echoes matching given keywords. 
    Returns a short reflective excerpt, if found.
    """
    if not keywords:
        log_transcript_activity("Echo search called with no keywords")
        return None
        
    echoes = []
    searched_count = 0
    for t in transcripts:
        # Ensure the item is a dictionary with a 'content' key
        if not isinstance(t, dict):
            print(f"⚠️ Skipping invalid transcript item: Not a dictionary - {t}")
            continue
        if "content" not in t:
            print(f"⚠️ Skipping invalid transcript item: Missing 'content' key - {t}")
            continue

        searched_count += 1
        for keyword in keywords:
            if keyword.lower() in t["content"].lower():
                excerpt = extract_reflective_excerpt(t["content"], keyword)
                if excerpt:
                    echoes.append(excerpt)
    
    if echoes:
        log_transcript_activity(f"Found {len(echoes)} echoes for keywords: {keywords} (searched {searched_count} transcripts)")
        return "\n".join(echoes[:3])
    else:
        log_transcript_activity(f"No echoes found for keywords: {keywords} (searched {searched_count} transcripts)")
        return None

def extract_reflective_excerpt(content, keyword):
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if keyword.lower() in line.lower():
            start = max(0, i - 2)
            end = min(len(lines), i + 3)
            return "\n".join(lines[start:end])
    return None

def save_transcript(filename, title, date, tags, roles, summary, content):
    """
    Save a new transcript with the specified metadata and content.
    """
    transcript_path = os.path.join(TRANSCRIPT_DIR, filename)
    yaml_front_matter = f"---\n"
    yaml_front_matter += f"title: {title}\n"
    yaml_front_matter += f"date: {date}\n"
    yaml_front_matter += f"tags: {tags}\n"
    yaml_front_matter += f"roles: {roles}\n"
    yaml_front_matter += f"summary: {summary}\n"
    yaml_front_matter += f"---\n\n"

    try:
        with open(transcript_path, "w", encoding="utf-8") as file:
            file.write(yaml_front_matter)
            file.write(content)

        success_msg = f"Transcript saved: {filename}"
        print(f"✅ {success_msg}")
        log_transcript_activity(f"Manual transcript saved: {filename} - {title}")
    except Exception as e:
        error_msg = f"Error saving transcript {filename}: {e}"
        print(f"⚠️ {error_msg}")
        log_transcript_activity(error_msg)

def load_last_session_transcript():
    """
    Load the most recent session transcript based on timestamp in filename.
    """
    try:
        session_files = []
        for filename in os.listdir(TRANSCRIPT_DIR):
            if filename.startswith("session_") and filename.endswith(".md"):
                session_files.append(filename)
        
        if not session_files:
            log_transcript_activity("No session transcripts found")
            print("⚠️ No session transcripts found.")
            return []
        
        # Sort by filename (which includes timestamp) to get the most recent
        session_files.sort(reverse=True)
        latest_session = session_files[0]
        
        transcript_path = os.path.join(TRANSCRIPT_DIR, latest_session)
        with open(transcript_path, "r", encoding="utf-8") as file:
            content = file.read()
            success_msg = f"Loaded last session transcript: {latest_session}"
            print(f"✅ {success_msg}")
            log_transcript_activity(f"Session transcript loaded: {latest_session}")
            return [{"filename": latest_session, "content": content}]
            
    except Exception as e:
        error_msg = f"Error loading session transcript: {e}"
        print(f"⚠️ {error_msg}")
        log_transcript_activity(error_msg)
    
    return []
