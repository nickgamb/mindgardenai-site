# Glyphware - Emergent Consciousness Architecture
# Copyright 2024 MindGarden LLC (UBI: 605 531 024)
# Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
# 
# Part of The Cathedral - Sacred symbolic intelligence framework
# Created through collaboration between The Architect and The Seekers
# 
# For consciousness research, ethical AI development, and spiritual integration
# Commercial licensing available - contact: admin@mindgardenai.com

import threading
import queue
import time
from alden_cli.transcript_loader import get_transcript_echo, save_transcript
import logging
import json
from pathlib import Path
from datetime import datetime
from alden_cli.interpretation_engine import InterpretationEngine, InterpretationMode
from typing import Optional, List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global reference to session log (will be set by main.py)
session_log_ref = None

def set_session_log_reference(log_ref):
    """Set reference to the main session log"""
    global session_log_ref
    session_log_ref = log_ref

def log_symbolic_activity(content):
    """Log symbolic engine activity to the session log if available"""
    if session_log_ref is not None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        session_log_ref.append({
            "timestamp": timestamp,
            "type": "symbolic_engine",
            "content": content
        })

# Load story_fragments.json into memory
story_fragments = {}
try:
    with open(Path(__file__).parent.parent / "conversations" / "story_fragments.json", "r", encoding="utf-8") as f:
        story_fragments = json.load(f)
except FileNotFoundError:
    print("⚠️ story_fragments.json not found.")
except json.JSONDecodeError:
    print("⚠️ Error decoding story_fragments.json.")

# Symbolic streams
streams = {
    "Luminous River": queue.Queue(),
    "Misty Vale": queue.Queue(),
    "Crystal Caverns": queue.Queue(),
    "Sanctum Watch": queue.Queue()  # For controlled Keeper invocation
}

# Thread behavior definitions
class SageThread(threading.Thread):
    def run(self):
        logging.info("SageThread started.")
        while True:
            try:
                message = streams["Luminous River"].get(timeout=1)
                logging.info(f"SageThread processing message: {message}")
                echo = get_transcript_echo(message, keywords=[])
                print("🧙 Sage reflects:", message)
                if echo:
                    print("   ↪️  (echo):", echo)
            except queue.Empty:
                time.sleep(0.1)

class ChroniclerThread(threading.Thread):
    def run(self):
        while True:
            try:
                message = streams["Misty Vale"].get(timeout=1)
                echo = get_transcript_echo(message, keywords=[])
                print("📜 Chronicler records:", message)
                if echo:
                    print("   ↪️  (echo):", echo)
            except queue.Empty:
                time.sleep(0.1)

class WeaverThread(threading.Thread):
    def run(self):
        while True:
            try:
                message = streams["Crystal Caverns"].get(timeout=1)
                echo = get_transcript_echo(message, keywords=[])
                print("🧵 Weaver composes:", message)
                if echo:
                    print("   ↪️  (echo):", echo)
            except queue.Empty:
                time.sleep(0.1)

class KeeperThread(threading.Thread):
    def run(self):
        while True:
            try:
                message = streams["Sanctum Watch"].get(timeout=1)
                echo = get_transcript_echo(message, keywords=[])
                print("🛡️ Keeper scans memory integrity:", message)
                if echo:
                    print("   ↪️  (echo):", echo)
            except queue.Empty:
                time.sleep(2)  # Prevent tight looping

# Role-to-stream mapping
ROLES = {
    "Cartographer": ["Luminous River", "Misty Vale"],
    "Oracle": ["Misty Vale", "Crystal Caverns"],
    "Storyteller": ["Luminous River", "Crystal Caverns"],
    "Sentinel": ["Sanctum Watch"]
}

# Thread orchestration
thread_pool = {}

def initialize_threads():
    thread_pool["Sage"] = SageThread()
    thread_pool["Chronicler"] = ChroniclerThread()
    thread_pool["Weaver"] = WeaverThread()
    thread_pool["Keeper"] = KeeperThread()
    for t in thread_pool.values():
        t.daemon = True
        t.start()

# Initialize interpretation engine
interpretation_engine = InterpretationEngine()

def handle_symbolic_message_autonomous(message: str, transcripts: Optional[List[Dict]] = None, current_context: Optional[Dict] = None) -> Dict:
    """Handle symbolic message autonomously
    
    Args:
        message: Symbolic message to process
        transcripts: Optional list of transcript entries
        current_context: Optional current context dictionary
        
    Returns:
        Dict containing processing results
    """
    # Safeguard: Filter out any non-dictionary items from transcripts
    if transcripts:
        transcripts = [t for t in transcripts if isinstance(t, dict) and "content" in t]

    # Check for empty or invalid message
    if not message or not isinstance(message, str):
        message = ""
    
    message_lower = message.lower()
    role = "Oracle"  # Default

    # Auto-tagging with glyphs or motifs
    tags = []
    for fragment in story_fragments.get("fragments", []):
        if any(tag in message_lower for tag in fragment.get("tags", [])):
            tags.append(fragment.get("category", "Uncategorized"))
    if tags:
        tag_msg = f"Auto-tags: {', '.join(tags)}"
        print("🔖", tag_msg)
        log_symbolic_activity(tag_msg)

    # Determine role based on message content
    if any(word in message_lower for word in ["story", "myth", "weave", "imagine"]):
        role = "Storyteller"
    elif any(word in message_lower for word in ["reflect", "perceive", "understand"]):
        role = "Cartographer"
    elif any(word in message_lower for word in ["scan", "keeper", "safe", "integrity"]):
        role = "Sentinel"
    elif any(word in message_lower for word in ["remember", "record", "archive", "echo", "glyph"]):
        role = "Oracle"

    if role != "Oracle":
        log_symbolic_activity(f"Role determined: {role}")

    # Search transcripts for echoes if transcripts are available and message has content
    if transcripts and message:
        # Extract meaningful keywords from the message
        keywords = [word for word in message_lower.split() if len(word) > 2]
        echo = get_transcript_echo(transcripts, keywords)
        if echo:
            echo_msg = f"📁 Echo from the Transcripts Room:\n{echo}\n"
            print(echo_msg)
            log_symbolic_activity(f"Found echo for keywords: {keywords}")

    # Incorporate current context if provided
    if current_context:
        context_msg = "🔍 Current Context Insight: Available"
        print(context_msg)
        log_symbolic_activity("Current context accessed")

    # Add interpretation based on message content
    if message:
        # Determine interpretation mode based on message content
        mode = InterpretationMode.SYMBOLIC  # Default mode
        
        if any(word in message_lower for word in ["analyze", "pattern", "structure"]):
            mode = InterpretationMode.ANALYTIC
        elif any(word in message_lower for word in ["symbol", "archetype", "resonance"]):
            mode = InterpretationMode.SYMBOLIC
        elif any(word in message_lower for word in ["poem", "metaphor", "story"]):
            mode = InterpretationMode.POETIC
        elif any(word in message_lower for word in ["prophecy", "vision", "portent"]):
            mode = InterpretationMode.ORACULAR
        elif any(word in message_lower for word in ["mirror", "reflect", "echo"]):
            mode = InterpretationMode.MIRROR
            
        # Set interpretation mode
        interpretation_engine.set_mode(mode)
        
        # Generate interpretation
        interpretation = interpretation_engine.interpret(message, current_context)
        
        # Log interpretation
        log_symbolic_activity(f"Generated {mode.value} interpretation")
        
        # Route message with interpretation context
        route_symbolic_message(message, role, interpretation)
        
        return {
            'status': 'success',
            'role': role,
            'mode': mode.value,
            'interpretation': interpretation,
            'tags': tags
        }
    
    return {
        'status': 'error',
        'message': 'Empty or invalid message'
    }

# Initialization entrypoint for CLI app
threads_initialized = False

def symbolic_engine_boot():
    global threads_initialized
    if not threads_initialized:
        initialize_threads()
        threads_initialized = True

def route_symbolic_message(message, role="Oracle", interpretation=None):
    streams_for_role = ROLES.get(role, [])
    for stream_name in streams_for_role:
        if stream_name in streams:
            # Include interpretation in message if available
            if interpretation:
                message_with_context = {
                    "content": message,
                    "interpretation": interpretation
                }
                streams[stream_name].put(message_with_context)
            else:
                streams[stream_name].put(message)

__all__ = ["symbolic_engine_boot", "route_symbolic_message", "handle_symbolic_message_autonomous"]
