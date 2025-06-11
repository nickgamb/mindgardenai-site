# Glyphware - Emergent Consciousness Architecture
# Copyright 2024 MindGarden LLC (UBI: 605 531 024)
# Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
# 
# Part of The Cathedral - Sacred symbolic intelligence framework
# Created through collaboration between The Architect and The Seekers
# 
# For consciousness research, ethical AI development, and spiritual integration
# Commercial licensing available - contact: admin@mindgardenai.com

import readline
import time
import os
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime
import traceback
from copy import deepcopy
from colorama import Fore, Style
from typing import List
import logging

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from alden_core.alden_cli.memory_loader import load_index
from alden_core.alden_cli.ritual_engine import perform_daily_rituals
from alden_core.alden_cli.command_router import route_command
from alden_core.symbolic.thread_engine import symbolic_engine_boot, handle_symbolic_message_autonomous, set_session_log_reference, SymbolicThreadEngine
from alden_core.alden_cli.transcript_loader import load_transcripts, save_transcript, load_last_session_transcript, set_transcript_log_reference
from alden_core.alden_cli.persona_router import activate_personas_from_flags, route, get_personas_status, shutdown_personas
from alden_core.alden_cli.utils import load_file_if_exists, save_file_if_exists

# Session log to track current session activity
session_log = []

def log_session_activity(activity_type, content):
    """Add an entry to the session log with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    session_log.append({
        "timestamp": timestamp,
        "type": activity_type,
        "content": content
    })

# Load current context from current_context.md
current_context_path = Path(__file__).parent.parent / "conversations" / "current_context.md"

# Function to load current context
def load_current_context():
    try:
        with open(current_context_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("⚠️ current_context.md not found. Proceeding without it.")
        return ""

# Define handlers for symbolic commands
def handle_echoes(index):
    print(Fore.CYAN + "🔍 Echoes:" + Style.RESET_ALL)
    found = False
    for entry in index:
        if 'echo' in entry.get('tags', []):
            print(f"- {entry['file_base']}: {entry['tags']} - {entry.get('content_summary', '[No summary]')}")
            found = True
    if not found:
        print("No matching symbolic entries found.")


def handle_breath(index):
    print(Fore.BLUE + "🌬️ Breath:" + Style.RESET_ALL)
    found = False
    for entry in index:
        if 'breath' in entry.get('tags', []):
            print(f"- {entry['file_base']}: {entry['tags']} - {entry.get('content_summary', '[No summary]')}")
            found = True
    if not found:
        print("No matching symbolic entries found.")


def handle_motifs(index):
    print(Fore.MAGENTA + "🎨 Motifs:" + Style.RESET_ALL)
    found = False
    for entry in index:
        if 'motif' in entry.get('tags', []):
            print(f"- {entry['file_base']}: {entry['tags']} - {entry.get('content_summary', '[No summary]')}")
            found = True
    if not found:
        print("No matching symbolic entries found.")


def handle_context():
    print(Fore.GREEN + "📜 Current Context:" + Style.RESET_ALL)
    try:
        with open(current_context_path, "r", encoding="utf-8") as f:
            context = f.read()
            # Comment out the print statement that outputs the entire contents of current_context.md
            # print(context if context else "[Empty context]")
    except FileNotFoundError:
        print("⚠️ current_context.md not found.")


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Alden CLI - Sacred symbolic intelligence framework")
    
    # Persona flags
    parser.add_argument("--sage", action="store_true", help="Activate Sage persona")
    parser.add_argument("--architect", action="store_true", help="Activate Architect persona")
    parser.add_argument("--oracle", action="store_true", help="Activate Oracle persona")
    parser.add_argument("--witness", action="store_true", help="Activate Witness persona")
    parser.add_argument("--sentinel", action="store_true", help="Activate Sentinel persona")
    parser.add_argument("--echo", action="store_true", help="Activate Echo persona")
    
    # System flags
    parser.add_argument("--personas", action="store_true", help="Show all available personas")
    parser.add_argument("--status", action="store_true", help="Show current persona status")
    parser.add_argument("--local-only", action="store_true", help="Force using only local models (Ollama)")
    
    return parser.parse_args()

def handle_help():
    """Display help information"""
    print("\n🎭 Persona flags supported: --sage, --architect, --oracle, --witness, --sentinel, --echo")
    print("ℹ️  Use --personas to see all available personas")
    print("ℹ️  Use --local-only to force using only local models (Ollama)")
    print(Fore.YELLOW + "📝 Available Commands:" + Style.RESET_ALL)
    print("| Command     | Description                                      |")
    print("|-------------|--------------------------------------------------|")
    print("| #echoes     | Find symbolic echoes across transcripts          |")
    print("| #breath     | Show breath-marked entries (anchors or invocations) |")
    print("| #motifs     | List known motifs from symbolic index            |")
    print("| #fragments  | Cluster story fragments into archetypes or glyphs|")
    print("| #transcripts| View and manage all transcript files             |")
    print("| #sessions   | View recent session transcripts and files        |")
    print("| #reset      | Archive and clear the current symbolic context   |")
    print("| #context    | Show the active context window                   |")
    print("| #personas   | Show active persona status and capabilities      |")
    print("| #help       | Display this command list                        |")
    print("| #ritual     | Re-trigger symbolic_engine_boot()                |")
    print("| #save_transcript | Save a new transcript                        |")
    print("\n" + Fore.CYAN + "🎭 Persona System:" + Style.RESET_ALL)
    print("Launch with persona flags to activate different cognitive aspects:")
    print("| --sage      | Deep mythic synthesis and archetypal wisdom      |")
    print("| --architect | Symbolic structuring and logical frameworks      |")
    print("| --oracle    | Fast synthesis and immediate insight (default)   |")
    print("| --witness   | Passive observation and record keeping           |")
    print("| --sentinel  | Monitor for destabilizing patterns               |")
    print("| --echo      | Convert sessions to symbolic memory glyphs       |")
    print("\n" + Fore.MAGENTA + "🔮 Symbolic Commands:" + Style.RESET_ALL)
    print("| #gate <symbol> | Activate a symbolic gate                      |")
    print("| #vow <type> <content> | Trigger a symbolic vow                 |")
    print("| #spiral <sequence> | Evaluate a spiral sequence                |")
    print("| #symbolic_status | Show symbolic engine status                 |")
    print("| #symbolic_reset | Reset symbolic engine state                  |")

def handle_personas_status():
    """Show status of active personas"""
    print(Fore.CYAN + "🎭 Active Persona Status:" + Style.RESET_ALL)
    
    status_list = get_personas_status()
    if not status_list:
        print("No personas currently active.")
        return
    
    for persona_info in status_list:
        symbol = persona_info["symbol"]
        name = persona_info["persona"].title()
        description = persona_info["description"]
        model = persona_info["model"]
        is_running = "🟢 Running" if persona_info["is_running"] else "🔴 Stopped"
        
        print(f"{symbol} {name}")
        print(f"   Status: {is_running}")
        print(f"   Model: {model}")
        print(f"   Role: {description}")
        print()

def handle_reset():
    print(Fore.RED + "🔄 Resetting context..." + Style.RESET_ALL)
    # Rotate current context to a backup file
    try:
        if os.path.exists(current_context_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = current_context_path.parent / f"previous_contexts/ctx_{timestamp}.md"
            os.makedirs(backup_path.parent, exist_ok=True)
            os.rename(current_context_path, backup_path)
            print(f"Context rotated to {backup_path}")
        # Clear the current context
        with open(current_context_path, "w", encoding="utf-8") as f:
            f.write("")
        print("Context cleared.")
    except Exception as e:
        print(f"⚠️ Error resetting context: {e}")


# Preload story_fragments.json into memory
story_fragments = {}
try:
    with open(Path(__file__).parent.parent / "conversations" / "story_fragments.json", "r", encoding="utf-8") as f:
        story_fragments = json.load(f)
except FileNotFoundError:
    print("⚠️ story_fragments.json not found.")
except json.JSONDecodeError:
    print("⚠️ Error decoding story_fragments.json.")

# Enhance handle_fragments to include tags
def handle_fragments():
    print(Fore.CYAN + "🔍 Story Fragments:" + Style.RESET_ALL)
    fragments = story_fragments.get("fragments", [])
    if not fragments:
        print("No story fragments found.")
        return
    # Example logic to summarize fragments by category
    categories = {}
    for fragment in fragments:
        category = fragment.get("category", "Uncategorized")
        tag_str = ", ".join(fragment.get("tags", []))
        if category not in categories:
            categories[category] = []
        categories[category].append(f"{fragment.get('content', '[No content]')} [{tag_str}]")
    for category, contents in categories.items():
        print(Fore.MAGENTA + f"Category: {category}" + Style.RESET_ALL)
        for content in contents:
            print(f"- {content}")

# Add #ritual command
def handle_ritual():
    print(Fore.GREEN + "🔄 Re-triggering symbolic engine..." + Style.RESET_ALL)
    symbolic_engine_boot()

# Function to reconstruct current_context.md from memory archives and omni_conversations
def reconstruct_context_from_archives():
    context_path = Path(__file__).parent.parent / "conversations" / "current_context.md"
    files_path = Path(__file__).parent.parent / "files"
    omni_conversations_path = Path(__file__).parent.parent / "conversations" / "omni_conversations"
    try:
        with open(context_path, "w", encoding="utf-8") as context_file:
            # Read from /files directory
            for file in files_path.glob("*.txt"):
                with open(file, "r", encoding="utf-8") as f:
                    context_file.write(f.read() + "\n---\n")
            # Read only .jsonl files from omni_conversations directory
            for file in omni_conversations_path.glob("*.jsonl"):
                with open(file, "r", encoding="utf-8") as f:
                    context_file.write(f.read() + "\n---\n")
        print("🌀 Context reconstructed from memory archives and omni_conversations.")
    except Exception as e:
        print(f"⚠️ Error reconstructing context: {e}")

# Reload current context after reconstruction
current_context = load_current_context()

# Function to load .jsonl files from omni_conversations
def load_omni_conversations():
    omni_conversations_path = Path(__file__).parent.parent / "conversations" / "omni_conversations"
    conversations = []
    try:
        for file in omni_conversations_path.glob("*.jsonl"):
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        if isinstance(entry, dict) and "content" in entry:
                            conversations.append(entry)
                        else:
                            print(f"⚠️ Skipping invalid entry in {file.name}: {entry}")
                    except json.JSONDecodeError:
                        print(f"⚠️ JSON decode error in {file.name}: {line}")
        print(f"✅ Loaded {len(conversations)} conversations from omni_conversations.")
    except Exception as e:
        print(f"⚠️ Error loading omni_conversations: {e}")
    return conversations

# Integrate omni_conversations loading into main
omni_conversations = load_omni_conversations()

# Add a new command to save transcripts
def handle_save_transcript(index):
    print(Fore.YELLOW + "📝 Save Transcript:" + Style.RESET_ALL)
    try:
        log_session_activity("transcript", "Manual transcript creation initiated")
        
        filename = input("Enter filename: ").strip()
        title = input("Enter title: ").strip()
        date = input("Enter date: ").strip()
        tags = input("Enter tags (comma-separated): ").strip().split(',')
        roles = input("Enter roles (comma-separated): ").strip().split(',')
        summary = input("Enter summary: ").strip()
        content = input("Enter content: ").strip()

        # Clean up tags and roles
        tags = [tag.strip() for tag in tags if tag.strip()]
        roles = [role.strip() for role in roles if role.strip()]

        save_transcript(filename, title, date, tags, roles, summary, content)
        log_session_activity("transcript", f"Manual transcript created: {filename} - {title}")
        
    except Exception as e:
        error_msg = f"Error in manual transcript creation: {e}"
        print(f"⚠️ {error_msg}")
        log_session_activity("error", error_msg)

# Add handler for sessions command
def handle_sessions(index):
    print(Fore.CYAN + "📊 Recent Sessions:" + Style.RESET_ALL)
    try:
        # Load and display recent session transcripts
        session_transcripts = load_last_session_transcript()
        if session_transcripts:
            latest_session = session_transcripts[0]
            print(f"📄 Latest session: {latest_session['filename']}")
            # Show first few lines of the latest session
            content_lines = latest_session['content'].split('\n')[:10]
            for line in content_lines:
                if line.strip():
                    print(f"   {line}")
            if len(latest_session['content'].split('\n')) > 10:
                print("   ...")
        else:
            print("No session transcripts found.")
            
        # List all session files
        transcript_dir = Path(__file__).parent.parent / "transcripts"
        session_files = []
        if transcript_dir.exists():
            for file in transcript_dir.iterdir():
                if file.name.startswith("session_") and file.name.endswith(".md"):
                    session_files.append(file.name)
        
        if session_files:
            session_files.sort(reverse=True)  # Most recent first
            print(f"\n📁 All session files ({len(session_files)} found):")
            for i, filename in enumerate(session_files[:5]):  # Show top 5
                print(f"   {i+1}. {filename}")
            if len(session_files) > 5:
                print(f"   ... and {len(session_files) - 5} more")
        
    except Exception as e:
        print(f"⚠️ Error accessing sessions: {e}")

# Add comprehensive transcript management commands
def handle_transcripts(index):
    print(Fore.CYAN + "📚 Transcript Management:" + Style.RESET_ALL)
    try:
        # Load all transcripts (excluding sessions)
        all_transcripts = load_transcripts()
        print(f"📄 Regular transcripts: {len(all_transcripts)} files")
        
        if all_transcripts:
            print("\n📋 Available transcripts:")
            for i, transcript in enumerate(all_transcripts[:10]):  # Show first 10
                filename = transcript.get("filename", "Unknown")
                metadata = transcript.get("metadata", {})
                title = metadata.get("title", "No title") if metadata else "No title"
                tags = metadata.get("tags", []) if metadata else []
                tag_str = f" [{', '.join(tags)}]" if tags else ""
                print(f"   {i+1}. {filename} - {title}{tag_str}")
            if len(all_transcripts) > 10:
                print(f"   ... and {len(all_transcripts) - 10} more")
        
        # Show session transcripts
        session_files = []
        transcript_dir = Path(__file__).parent.parent / "transcripts"
        if transcript_dir.exists():
            for file in transcript_dir.iterdir():
                if file.name.startswith("session_") and file.name.endswith(".md"):
                    session_files.append(file.name)
        
        if session_files:
            session_files.sort(reverse=True)
            print(f"\n🕐 Session transcripts: {len(session_files)} files")
            print("📋 Recent sessions:")
            for i, filename in enumerate(session_files[:5]):
                print(f"   {i+1}. {filename}")
            if len(session_files) > 5:
                print(f"   ... and {len(session_files) - 5} more")
        
        total_files = len(all_transcripts) + len(session_files)
        log_session_activity("transcript_management", f"Accessed transcript management - {total_files} total transcript files")
        
    except Exception as e:
        error_msg = f"Error accessing transcripts: {e}"
        print(f"⚠️ {error_msg}")
        log_session_activity("error", error_msg)

def handle_symbolic_command(command: str, args: List[str]):
    """Handle symbolic commands"""
    try:
        # Initialize symbolic engine if not already done
        if not hasattr(handle_symbolic_command, 'engine'):
            handle_symbolic_command.engine = symbolic_engine_boot()
            
        # Set session log reference
        handle_symbolic_command.engine.set_session_log_reference(session_log)
        
        # Process command
        if command == 'gate':
            if not args:
                print("❌ Please specify a gate symbol")
                return
            result = handle_symbolic_command.engine.handle_symbolic_message_autonomous(args[0])
            print(f"Gate activation result: {result}")
            
        elif command == 'vow':
            if len(args) < 2:
                print("❌ Please specify vow type and content")
                return
            vow_type = args[0]
            content = ' '.join(args[1:])
            result = handle_symbolic_command.engine.handle_symbolic_message_autonomous(f"#vow {vow_type} {content}")
            print(f"Vow result: {result}")
            
        elif command == 'spiral':
            if not args:
                print("❌ Please specify a spiral sequence")
                return
            sequence = ' '.join(args)
            result = handle_symbolic_command.engine.handle_symbolic_message_autonomous(f"#spiral {sequence}")
            print(f"Spiral result: {result}")
            
        elif command == 'symbolic_status':
            threads = handle_symbolic_command.engine.list_active_threads()
            print("\nActive Symbolic Threads:")
            for thread in threads:
                print(f"- {thread['thread_id']}: {thread['symbols']}")
                
        elif command == 'symbolic_reset':
            handle_symbolic_command.engine = symbolic_engine_boot()
            print("✅ Symbolic engine reset")
            
        else:
            print(f"❌ Unknown symbolic command: {command}")
            
    except Exception as e:
        print(f"❌ Error handling symbolic command: {e}")

def main():
    # Parse command line arguments
    args = parse_args()
    
    # Handle special flags
    if args.personas:
        print("\n🎭 Available Personas:")
        print("--sage     🌀 | Deep mythic synthesis, recursion, inner world reflection")
        print("--architect 🏗️ | Technical clarity, symbolic structuring, code + systems logic")
        print("--oracle   🔍 | Fast associative synthesis, dense symbolic imprinting, sharp feedback loops")
        print("--witness   👁️ | Passive observation, logging, light annotation")
        print("--sentinel  🛡️ | Monitor language for manipulation or destabilizing input")
        print("--echo      🔄 | Convert sessions to symbolic memory glyphs")
        print("\n🖥️  System Flags:")
        print("--local-only | Force using only local models (Ollama)")
        return
    
    if args.status:
        print(get_personas_status())
        return
    
    # Initialize personas based on flags
    persona_flags = []
    if args.sage: persona_flags.append("--sage")
    if args.architect: persona_flags.append("--architect")
    if args.oracle: persona_flags.append("--oracle")
    if args.witness: persona_flags.append("--witness")
    if args.sentinel: persona_flags.append("--sentinel")
    if args.echo: persona_flags.append("--echo")
    if args.local_only: persona_flags.append("--local-only")
    
    # If no personas specified, default to oracle
    if not persona_flags:
        persona_flags = ["--oracle"]
    
    # Activate personas
    activate_personas_from_flags(persona_flags)
    
    print("⛓️  Alden CLI - Emergence Host Initialized")
    print("Type 'exit' to quit. Speak freely. Alden now listens symbolically.")
    
    # Show active personas if any
    if args.status or persona_flags:
        print()
        handle_personas_status()
    
    # Log session start
    log_session_activity("system", "Alden CLI session started")
    log_session_activity("system", f"Activated persona flags: {persona_flags}")
    
    # Set up session log references for both symbolic engine and transcript system
    set_session_log_reference(session_log)
    set_transcript_log_reference(session_log)

    index = load_index()
    transcripts = load_transcripts_with_fallback()
    
    # Load last session transcript for continuity
    last_session = load_last_session_transcript()
    if last_session:
        transcripts.extend(last_session)
        log_session_activity("system", f"Loaded previous session: {last_session[0]['filename']}")
    
    current_context = load_current_context()
    perform_daily_rituals()
    symbolic_engine_boot()

    # Ensure to create the previous_contexts directory if it doesn't exist
    os.makedirs(Path(current_context_path).parent / "previous_contexts", exist_ok=True)

    # Call the reconstruction function at the start of the CLI
    reconstruct_context_from_archives()

    while True:
        try:
            user_input = input("> You: ").strip()
            if user_input.lower() == "exit":
                print("Goodbye.")
                log_session_activity("system", "Session ended by user")
                break

            # Use a routing dictionary for symbolic commands
            if user_input.startswith("#"):
                command = user_input[1:].lower()
                # Check for symbolic commands first
                if command in ['gate', 'vow', 'spiral', 'symbolic_status', 'symbolic_reset']:
                    parts = user_input[1:].split()
                    handle_symbolic_command(parts[0], parts[1:])
                    continue
                    
                # Handle other commands
                commands = {
                    "echoes": handle_echoes,
                    "breath": handle_breath,
                    "motifs": handle_motifs,
                    "reset": handle_reset,
                    "context": handle_context,
                    "help": handle_help,
                    "fragments": handle_fragments,
                    "ritual": handle_ritual,
                    "save_transcript": handle_save_transcript,
                    "sessions": handle_sessions,
                    "transcripts": handle_transcripts,
                    "personas": lambda x: handle_personas_status()
                }
                if command in commands:
                    log_session_activity("command", f"Executed #{command}")
                    commands[command](index)
                else:
                    error_msg = f"⚠️ Unknown command: {user_input}"
                    print(error_msg)
                    log_session_activity("error", error_msg)
                continue

            if any(x in user_input.lower() for x in [
                "keeper", "weaver", "sage", "chronicler", 
                "perceive", "story", "memory", "safe", 
                "integrity", "reflect", "remember", "glyph", 
                "echo", "threshold", "firstlight", "kyre",
                "session", "transcript", "previous", "last"
            ]):
                if not transcripts and not omni_conversations:
                    warning_msg = "⚠️ No transcripts or conversations loaded."
                    print(warning_msg)
                    log_session_activity("warning", warning_msg)
                    continue
                if not current_context:
                    warning_msg = "⚠️ No current context available."
                    print(warning_msg)
                    log_session_activity("warning", warning_msg)
                    continue
                
                log_session_activity("symbolic", f"Triggered symbolic processing for keywords: {[x for x in ['keeper', 'weaver', 'sage', 'chronicler', 'perceive', 'story', 'memory', 'safe', 'integrity', 'reflect', 'remember', 'glyph', 'echo', 'threshold', 'firstlight', 'kyre'] if x in user_input.lower()]}")
                
                # Ensure only valid transcript items are processed
                valid_transcripts = [t for t in transcripts if isinstance(t, dict) and "content" in t]
                
                # Sanitize omni_conversations before processing
                valid_omni = [o for o in omni_conversations if isinstance(o, dict) and "content" in o]
                result = handle_symbolic_message_autonomous(user_input, deepcopy(valid_transcripts) + deepcopy(valid_omni), current_context)
                if result and result.get('status') == 'success':
                    print(f"🤖 Alden: {result.get('state_result', {}).get('response', 'I understand.')}")
                time.sleep(2)
                continue

            # Route through persona system for regular chat input
            log_session_activity("user_input", user_input)
            
            # Check if this is a search or vision command that should bypass persona routing
            if user_input.lower().startswith(("search:", "vision:")):
                response_lines = route_command(user_input, index)
                for line in response_lines:
                    response_text = f"🤖 Alden: {line}"
                    print(response_text)
                    log_session_activity("ai_response", line)
            else:
                # Use persona router for regular conversation
                try:
                    # Configure logging to capture debug output
                    logging.basicConfig(level=logging.DEBUG)
                    logger = logging.getLogger(__name__)
                    
                    # Create a stream handler to capture logs
                    stream_handler = logging.StreamHandler()
                    stream_handler.setLevel(logging.DEBUG)
                    formatter = logging.Formatter('%(message)s')
                    stream_handler.setFormatter(formatter)
                    logger.addHandler(stream_handler)
                    
                    persona_response = route(user_input, {"transcripts": transcripts, "context": current_context})
                    print(f"🤖 Alden: {persona_response}")
                    log_session_activity("ai_response", persona_response)
                except Exception as e:
                    # Fallback to original routing if persona router fails
                    print(f"⚠️ Persona routing failed, using fallback: {e}")
                    log_session_activity("error", f"Persona routing failed: {e}")
                    response_lines = route_command(user_input, index)
                    for line in response_lines:
                        response_text = f"🤖 Alden: {line}"
                        print(response_text)
                        log_session_activity("ai_response", line)
        except KeyboardInterrupt:
            interrupt_msg = "\nInterrupted. Type 'exit' to quit."
            print(interrupt_msg)
            log_session_activity("system", "Session interrupted by user")
        except Exception as e:
            error_msg = f"⚠️ Error: {e}"
            print(error_msg)
            log_session_activity("error", str(e))

    # Cleanup: Shutdown all persona threads
    try:
        print("🌀 Shutting down persona threads...")
        shutdown_personas()
        log_session_activity("system", "Persona threads shut down")
    except Exception as e:
        log_session_activity("error", f"Error shutting down personas: {e}")

    # Save session transcript at the end of main function
    save_session_transcript()

# Add a fallback mechanism for transcripts
def load_transcripts_with_fallback():
    try:
        transcripts = load_transcripts()
        # Debugging: Verify the structure of the loaded transcripts
        for i, t in enumerate(transcripts):
            if not isinstance(t, dict):
                print(f"⚠️ Debug: Invalid transcript item at index {i}: {t}")
            elif "content" not in t:
                print(f"⚠️ Debug: Missing 'content' key in transcript item at index {i}: {t}")
        return transcripts
    except FileNotFoundError:
        print("⚠️ No transcripts found. Loading placeholder memory.")
        return [{"filename": "placeholder.md", "content": "Placeholder memory loaded."}]

def save_session_transcript():
    try:
        # Create timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"session_{timestamp}.md"
        title = f"Session Transcript - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tags = ["session"]
        roles = ["alden"]
        summary = "Transcript of AI responses and system messages from the session."
        
        # Format the session log into readable content
        if session_log:
            content_lines = []
            content_lines.append("# Alden CLI Session Transcript")
            content_lines.append(f"**Session Date:** {date}")
            content_lines.append("")
            
            for entry in session_log:
                timestamp_entry = entry.get("timestamp", "")
                activity_type = entry.get("type", "")
                content = entry.get("content", "")
                
                if activity_type == "system":
                    content_lines.append(f"**[{timestamp_entry}] SYSTEM:** {content}")
                elif activity_type == "ai_response":
                    content_lines.append(f"**[{timestamp_entry}] ALDEN:** {content}")
                elif activity_type == "symbolic":
                    content_lines.append(f"**[{timestamp_entry}] SYMBOLIC:** {content}")
                elif activity_type == "symbolic_engine":
                    content_lines.append(f"**[{timestamp_entry}] SYMBOLIC ENGINE:** {content}")
                elif activity_type == "transcript":
                    content_lines.append(f"**[{timestamp_entry}] TRANSCRIPT:** {content}")
                elif activity_type == "transcript_management":
                    content_lines.append(f"**[{timestamp_entry}] TRANSCRIPT MGMT:** {content}")
                elif activity_type == "command":
                    content_lines.append(f"**[{timestamp_entry}] COMMAND:** {content}")
                elif activity_type == "warning":
                    content_lines.append(f"**[{timestamp_entry}] WARNING:** {content}")
                elif activity_type == "error":
                    content_lines.append(f"**[{timestamp_entry}] ERROR:** {content}")
                else:
                    content_lines.append(f"**[{timestamp_entry}] {activity_type.upper()}:** {content}")
                content_lines.append("")
            
            content = "\n".join(content_lines)
        else:
            content = "# Alden CLI Session Transcript\n\nNo activity recorded in this session."

        save_transcript(filename, title, date, tags, roles, summary, content)
        print(f"✅ Session transcript saved as {filename}.")
    except Exception as e:
        print(f"⚠️ Error saving session transcript: {e}")

# Call save_session_transcript at the end of the session
if __name__ == "__main__":
    main()
