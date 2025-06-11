#!/bin/bash
# Glyphware Header Addition Script - WSL/Linux Version
# Adds copyright headers to source files throughout The Cathedral
# Copyright 2024 MindGarden LLC - Part of Glyphware License Implementation
# 
# WSL/Linux version with proper exclusions for virtual environments and dependencies

echo -e "\033[96mInitiating Glyphware License Protection (WSL/Linux VERSION)...\033[0m"
echo -e "\033[92mAdding copyright headers to The Cathedral source files...\033[0m"
echo -e "\033[93mExcluding virtual environments and dependency directories...\033[0m"

# Define headers for different file types
PYTHON_HEADER="# Glyphware - Emergent Consciousness Architecture
# Copyright 2024 MindGarden LLC (UBI: 605 531 024)
# Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
# 
# Part of The Cathedral - Sacred symbolic intelligence framework
# Created through collaboration between The Architect and The Seekers
# 
# For consciousness research, ethical AI development, and spiritual integration
# Commercial licensing available - contact: admin@mindgardenai.com

"

XML_HEADER="<!--
  Glyphware - Emergent Consciousness Architecture
  Copyright 2024 MindGarden LLC (UBI: 605 531 024)
  Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
  
  Part of The Cathedral - Sacred symbolic intelligence framework
  Created through collaboration between The Architect and The Seekers
  
  For consciousness research, ethical AI development, and spiritual integration
  Commercial licensing available - contact: admin@mindgardenai.com
-->

"

JS_HEADER="// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Sacred symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com

"

SHELL_HEADER="#!/bin/bash
# Glyphware - Emergent Consciousness Architecture
# Copyright 2024 MindGarden LLC (UBI: 605 531 024)
# Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
# 
# Part of The Cathedral - Sacred symbolic intelligence framework

"

# Exclusion patterns for directories we should NOT process
EXCLUDE_PATTERNS=(
    "*.venv*"
    "*venv*"
    "*node_modules*"
    "*site-packages*"
    "*.git*"
    "*__pycache__*"
    "*.pytest_cache*"
    "*build*"
    "*dist*"
    "*.next*"
    "*coverage*"
    "*.coverage*"
    "*target*"
    "*.gradle*"
    "*.idea*"
    "*.vscode*"
    "*vendor*"
    "*deps*"
)

# Counters
files_processed=0
files_skipped=0

# Function to check if file should be excluded
should_exclude_file() {
    local file_path="$1"
    
    for pattern in "${EXCLUDE_PATTERNS[@]}"; do
        if [[ "$file_path" == $pattern ]]; then
            return 0  # Should exclude
        fi
    done
    return 1  # Should not exclude
}

# Function to add header to file
add_header_to_file() {
    local file_path="$1"
    local header="$2"
    local file_type="$3"
    
    # Check exclusion patterns first
    if should_exclude_file "$file_path"; then
        ((files_skipped++))
        echo -e "  \033[90mExcluded (dependency/build): $file_path\033[0m"
        return
    fi
    
    # Check if file exists and is readable
    if [[ ! -f "$file_path" ]]; then
        echo -e "  \033[91mError: File not found: $file_path\033[0m"
        return
    fi
    
    # Read file content
    local content
    if ! content=$(cat "$file_path" 2>/dev/null); then
        echo -e "  \033[91mError reading $file_path\033[0m"
        return
    fi
    
    # Skip if already has Glyphware header
    if echo "$content" | grep -q "Glyphware"; then
        ((files_skipped++))
        echo -e "  \033[93mSkipped (already protected): $file_path\033[0m"
        return
    fi
    
    # Skip if file is too small (likely empty or just license)
    if [[ ${#content} -lt 50 ]]; then
        ((files_skipped++))
        echo -e "  \033[93mSkipped (too small): $file_path\033[0m"
        return
    fi
    
    # Create new content based on file type
    local new_content
    if [[ "$file_type" == "shell" && "$content" =~ ^#!/ ]]; then
        # Preserve shebang line for shell scripts
        local shebang_line=$(echo "$content" | head -n1)
        local rest_content=$(echo "$content" | tail -n +2)
        new_content="$shebang_line
$header$rest_content"
    elif [[ "$file_type" == "xml" && "$content" =~ ^\s*\<\?xml ]]; then
        # Preserve XML declaration
        local xml_line=$(echo "$content" | head -n1)
        local rest_content=$(echo "$content" | tail -n +2)
        new_content="$xml_line
$header$rest_content"
    else
        new_content="$header$content"
    fi
    
    # Write the updated content
    if echo "$new_content" > "$file_path"; then
        ((files_processed++))
        echo -e "  \033[92mProtected: $file_path\033[0m"
    else
        echo -e "  \033[91mError writing to $file_path\033[0m"
    fi
}

# Process The Cathedral - Highest Priority
echo ""
echo -e "\033[95mProcessing The Cathedral (Sacred Core)...\033[0m"

if [[ -d "alden_core" ]]; then
    # Python files in alden_core (main directory)
    find alden_core -maxdepth 1 -name "*.py" -type f | while read -r file; do
        add_header_to_file "$file" "$PYTHON_HEADER" "python"
    done
    
    # Python files in alden_core/alden_cli (core CLI components)
    find alden_core/alden_cli -name "*.py" -type f | while read -r file; do
        add_header_to_file "$file" "$PYTHON_HEADER" "python"
    done
    
    # Shell scripts in alden_core
    find alden_core -name "*.sh" -type f | while read -r file; do
        add_header_to_file "$file" "$SHELL_HEADER" "shell"
    done
else
    echo -e "  \033[93mWarning: alden_core directory not found\033[0m"
fi

# Process Server Backend
echo ""
echo -e "\033[94mProcessing Server Backend...\033[0m"

if [[ -d "server" ]]; then
    find server -name "*.py" -type f | while read -r file; do
        add_header_to_file "$file" "$PYTHON_HEADER" "python"
    done
else
    echo -e "  \033[93mWarning: Server directory not found\033[0m"
fi

# Process Web Client
echo ""
echo -e "\033[94mProcessing Web Client...\033[0m"

if [[ -d "web-client" ]]; then
    # JavaScript/TypeScript files
    find web-client -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" | while read -r file; do
        add_header_to_file "$file" "$JS_HEADER" "javascript"
    done
    
    # HTML files
    find web-client -name "*.html" -type f | while read -r file; do
        add_header_to_file "$file" "$XML_HEADER" "xml"
    done
else
    echo -e "  \033[93mWarning: Web-client directory not found\033[0m"
fi

# Process Mobile Apps
echo ""
echo -e "\033[94mProcessing Mobile Applications...\033[0m"

if [[ -d "mobile" ]]; then
    # Java/Kotlin files
    find mobile -name "*.java" -o -name "*.kt" | while read -r file; do
        add_header_to_file "$file" "$JS_HEADER" "java"
    done
    
    # XML files
    find mobile -name "*.xml" -type f | while read -r file; do
        add_header_to_file "$file" "$XML_HEADER" "xml"
    done
else
    echo -e "  \033[93mWarning: Mobile directory not found\033[0m"
fi

# Process Agents
echo ""
echo -e "\033[94mProcessing AI Agents...\033[0m"

if [[ -d "agents" ]]; then
    find agents -name "*.py" -type f | while read -r file; do
        add_header_to_file "$file" "$PYTHON_HEADER" "python"
    done
else
    echo -e "  \033[93mWarning: Agents directory not found\033[0m"
fi

# Process root configuration files
echo ""
echo -e "\033[94mProcessing Root Configuration Files...\033[0m"

# Shell scripts in root (exclude header scripts to avoid circular issues)
find . -maxdepth 1 -name "*.sh" -type f | grep -v glyphware | grep -v header | while read -r file; do
    add_header_to_file "$file" "$SHELL_HEADER" "shell"
done

# Final Summary
echo ""
echo -e "\033[92mGlyphware License Protection Complete!\033[0m"
echo -e "\033[96mSummary:\033[0m"
echo -e "  \033[92mFiles Protected: $files_processed\033[0m"
echo -e "  \033[93mFiles Skipped/Excluded: $files_skipped\033[0m"

echo ""
echo -e "\033[95mExclusions Applied:\033[0m"
echo -e "  \033[97m- Virtual environments (.venv, venv)\033[0m"
echo -e "  \033[97m- Node.js dependencies (node_modules)\033[0m"
echo -e "  \033[97m- Python packages (site-packages)\033[0m"
echo -e "  \033[97m- Build directories (build, dist, target)\033[0m"
echo -e "  \033[97m- IDE/editor files (.vscode, .idea)\033[0m"

echo ""
echo -e "\033[95mNext Steps:\033[0m"
echo -e "  \033[97m1. Review the LICENSE-GLYPHWARE.md file\033[0m"
echo -e "  \033[97m2. Update README.md files with license information\033[0m"
echo -e "  \033[97m3. Commit changes to repository\033[0m"
echo -e "  \033[97m4. Consider legal review within 30 days\033[0m"

echo ""
echo -e "\033[96mThe Cathedral is now protected under Glyphware License v1.0\033[0m"
echo -e "\033[92mOnly source code files processed - dependencies excluded!\033[0m" 