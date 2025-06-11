#!/bin/bash
#!/bin/bash
# Glyphware - Emergent Consciousness Architecture
# Copyright 2024 MindGarden LLC (UBI: 605 531 024)
# Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
# 
# Part of The Cathedral - Sacred symbolic intelligence framework


# Alden CLI API Key Setup Script
echo "🔑 Setting up API keys for Alden CLI Persona System"
echo "=================================================="

# Create .env file if it doesn't exist
ENV_FILE=".env"

# Function to update or add a key in .env file
update_env_key() {
    local key_name="$1"
    local key_value="$2"
    local comment="$3"
    
    if [ -f "$ENV_FILE" ]; then
        # Check if key already exists (commented or uncommented)
        if grep -q "^#\?${key_name}=" "$ENV_FILE"; then
            # Key exists, update it
            if [ -n "$key_value" ]; then
                # Replace with new value (uncommented)
                sed -i "s|^#\?${key_name}=.*|${key_name}=\"${key_value}\"|" "$ENV_FILE"
                echo "✅ Updated $key_name"
            else
                # Comment out the key
                sed -i "s|^${key_name}=.*|# ${key_name}=\"your-key-here\"|" "$ENV_FILE"
                echo "⏩ $key_name left commented"
            fi
        else
            # Key doesn't exist, add it
            if [ -n "$key_value" ]; then
                echo "${key_name}=\"${key_value}\"" >> "$ENV_FILE"
                echo "✅ Added $key_name"
            else
                echo "# ${key_name}=\"your-key-here\"" >> "$ENV_FILE"
                echo "⏩ Added $key_name (commented)"
            fi
        fi
    else
        # No .env file, create it
        echo "# Alden CLI API Keys" > "$ENV_FILE"
        echo "# Generated on $(date)" >> "$ENV_FILE"
        echo "" >> "$ENV_FILE"
        
        if [ -n "$key_value" ]; then
            echo "${key_name}=\"${key_value}\"" >> "$ENV_FILE"
            echo "✅ Added $key_name"
        else
            echo "# ${key_name}=\"your-key-here\"" >> "$ENV_FILE"
            echo "⏩ Added $key_name (commented)"
        fi
    fi
}

# Function to get current key value
get_current_key() {
    local key_name="$1"
    if [ -f "$ENV_FILE" ]; then
        # Extract current value (if uncommented)
        grep "^${key_name}=" "$ENV_FILE" 2>/dev/null | cut -d'"' -f2
    fi
}

echo "This script will help you configure API keys for different AI providers."
echo "Keys will be stored in a .env file and loaded as environment variables."
echo ""

# Check if .env already exists
if [ -f "$ENV_FILE" ]; then
    echo "📄 Found existing .env file. Will update individual keys as needed."
    echo "   Creating backup at .env.backup"
    cp "$ENV_FILE" ".env.backup"
else
    echo "📄 Creating new .env file"
fi

echo ""

# OpenAI API Key
current_openai=$(get_current_key "OPENAI_API_KEY")
echo "🤖 OpenAI API Key (for Sage, Architect, Oracle, Sentinel personas)"
echo "   Get your key from: https://platform.openai.com/api-keys"
if [ -n "$current_openai" ]; then
    echo "   Current: ${current_openai:0:10}...${current_openai: -4}"
    echo -n "   Enter new key (or press Enter to keep current): "
else
    echo -n "   Enter your OpenAI API key (or press Enter to skip): "
fi
read -r openai_key

# If user pressed enter and we have a current key, keep it
if [ -z "$openai_key" ] && [ -n "$current_openai" ]; then
    echo "⏩ Keeping existing OpenAI key"
else
    update_env_key "OPENAI_API_KEY" "$openai_key"
fi

echo ""

# Anthropic API Key
current_anthropic=$(get_current_key "ANTHROPIC_API_KEY")
echo "🧠 Anthropic API Key (for Witness, Echo personas)"
echo "   Get your key from: https://console.anthropic.com/settings/keys"
if [ -n "$current_anthropic" ]; then
    echo "   Current: ${current_anthropic:0:10}...${current_anthropic: -4}"
    echo -n "   Enter new key (or press Enter to keep current): "
else
    echo -n "   Enter your Anthropic API key (or press Enter to skip): "
fi
read -r anthropic_key

# If user pressed enter and we have a current key, keep it
if [ -z "$anthropic_key" ] && [ -n "$current_anthropic" ]; then
    echo "⏩ Keeping existing Anthropic key"
else
    update_env_key "ANTHROPIC_API_KEY" "$anthropic_key"
fi

echo ""

# Ollama API configuration (for fallbacks)
current_ollama=$(get_current_key "OLLAMA_API_URL")
echo "🦙 Ollama API URL (for local model fallbacks)"
echo "   Default: http://localhost:11434"
if [ -n "$current_ollama" ]; then
    echo "   Current: $current_ollama"
    echo -n "   Enter new URL (or press Enter to keep current): "
else
    echo -n "   Enter Ollama URL (or press Enter for default): "
fi
read -r ollama_url

if [ -z "$ollama_url" ] && [ -n "$current_ollama" ]; then
    echo "⏩ Keeping existing Ollama URL"
elif [ -z "$ollama_url" ]; then
    update_env_key "OLLAMA_API_URL" "http://localhost:11434"
else
    update_env_key "OLLAMA_API_URL" "$ollama_url"
fi

echo ""
echo "📝 Configuration saved to .env file"
echo ""

# Show current configuration summary
echo "🔍 Current API Key Status:"
if [ -f "$ENV_FILE" ]; then
    if grep -q "^OPENAI_API_KEY=" "$ENV_FILE"; then
        echo "   ✅ OpenAI API Key: configured"
    else
        echo "   ❌ OpenAI API Key: not set"
    fi
    
    if grep -q "^ANTHROPIC_API_KEY=" "$ENV_FILE"; then
        echo "   ✅ Anthropic API Key: configured"
    else
        echo "   ❌ Anthropic API Key: not set"
    fi
    
    if grep -q "^OLLAMA_API_URL=" "$ENV_FILE"; then
        echo "   ✅ Ollama URL: configured"
    else
        echo "   ❌ Ollama URL: not set"
    fi
fi

echo ""
echo "🚀 To use the API keys, run:"
echo "   source .env && ./start.sh [persona-flags]"
echo ""
echo "💡 Example usage:"
echo "   source .env && ./start.sh --sage --oracle --architect"
echo ""
echo "🔒 Security note: .env file contains sensitive keys. Don't commit it to version control!"

# Add .env to .gitignore if git repo exists
if [ -d ".git" ]; then
    if ! grep -q "^\.env$" .gitignore 2>/dev/null; then
        echo ".env" >> .gitignore
        echo "✅ Added .env to .gitignore"
    fi
fi 
