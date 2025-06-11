#!/bin/bash
# Glyphware - Emergent Consciousness Architecture
# Copyright 2024 MindGarden LLC (UBI: 605 531 024)
# Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
# 
# Part of The Cathedral - Sacred symbolic intelligence framework

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Get the project root directory (parent of alden_core)
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

echo "🌀 Starting Alden CLI..."

# Check for Ollama installation
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed. Please install it from https://ollama.com/download and try again."
    exit 1
fi

# Start Ollama service if not running
if ! pgrep -x "ollama" > /dev/null; then
    echo "🚀 Starting Ollama service..."
    nohup ollama serve > /dev/null 2>&1 &
    sleep 3
fi

# Ensure LLaMA3 model is available
if ! ollama list | grep -q "llama3"; then
    echo "⬇️  Pulling LLaMA3 model from Ollama..."
    ollama pull llama3
fi

# Check and activate Python virtual environment
if [ ! -f "$PROJECT_ROOT/.venv/bin/activate" ]; then
    echo "❌ Python virtual environment not found. Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source "$PROJECT_ROOT/.venv/bin/activate"

# Add project root to PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Change to project root directory
cd "$PROJECT_ROOT"

# Launch Alden CLI with all command line arguments passed through
echo "🎭 Persona flags supported: --sage, --architect, --oracle, --witness, --sentinel, --echo"
echo "ℹ️  Use --personas to see all available personas"
python3 -m alden_core.alden_cli.main "$@" 
