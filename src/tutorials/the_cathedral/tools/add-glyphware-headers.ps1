# Glyphware Header Addition Script - FIXED VERSION
# Adds copyright headers to source files throughout The Cathedral
# Copyright 2024 MindGarden LLC - Part of Glyphware License Implementation
# 
# FIXED: Now excludes virtual environments and dependency directories

Write-Host "Initiating Glyphware License Protection (FIXED VERSION)..." -ForegroundColor Cyan
Write-Host "Adding copyright headers to The Cathedral source files..." -ForegroundColor Green
Write-Host "Excluding virtual environments and dependency directories..." -ForegroundColor Yellow

# Define headers for different file types
$pythonHeader = @"
# Glyphware - Emergent Consciousness Architecture
# Copyright 2024 MindGarden LLC (UBI: 605 531 024)
# Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
# 
# Part of The Cathedral - Sacred symbolic intelligence framework
# Created through collaboration between The Architect and The Seekers
# 
# For consciousness research, ethical AI development, and spiritual integration
# Commercial licensing available - contact: admin@mindgardenai.com

"@

$xmlHeader = @"
<!--
  Glyphware - Emergent Consciousness Architecture
  Copyright 2024 MindGarden LLC (UBI: 605 531 024)
  Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
  
  Part of The Cathedral - Sacred symbolic intelligence framework
  Created through collaboration between The Architect and The Seekers
  
  For consciousness research, ethical AI development, and spiritual integration
  Commercial licensing available - contact: admin@mindgardenai.com
-->

"@

$jsHeader = @"
// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Sacred symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com

"@

$shellHeader = @"
#!/bin/bash
# Glyphware - Emergent Consciousness Architecture
# Copyright 2024 MindGarden LLC (UBI: 605 531 024)
# Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
# 
# Part of The Cathedral - Sacred symbolic intelligence framework

"@

# Exclusion patterns for directories we should NOT process
$excludePatterns = @(
    "*\.venv\*",
    "*\venv\*", 
    "*\node_modules\*",
    "*\site-packages\*",
    "*\.git\*",
    "*\__pycache__\*",
    "*\.pytest_cache\*",
    "*\build\*",
    "*\dist\*",
    "*\.next\*",
    "*\coverage\*",
    "*\.coverage\*",
    "*\target\*",
    "*\.gradle\*",
    "*\.idea\*",
    "*\.vscode\*",
    "*\vendor\*",
    "*\deps\*"
)

# Counters
$filesProcessed = 0
$filesSkipped = 0

# Function to check if file should be excluded
function Should-ExcludeFile {
    param([string]$FilePath)
    
    foreach ($pattern in $excludePatterns) {
        if ($FilePath -like $pattern) {
            return $true
        }
    }
    return $false
}

# Function to add header to file
function Add-HeaderToFile {
    param(
        [string]$FilePath,
        [string]$Header,
        [string]$FileType
    )
    
    # Check exclusion patterns first
    if (Should-ExcludeFile -FilePath $FilePath) {
        $script:filesSkipped++
        Write-Host "  Excluded (dependency/build): $FilePath" -ForegroundColor DarkYellow
        return
    }
    
    try {
        $content = Get-Content $FilePath -Raw -ErrorAction Stop
        
        # Skip if already has Glyphware header
        if ($content -match "Glyphware") {
            $script:filesSkipped++
            Write-Host "  Skipped (already protected): $FilePath" -ForegroundColor Yellow
            return
        }
        
        # Skip if file is too small (likely empty or just license)
        if ($content.Length -lt 50) {
            $script:filesSkipped++
            Write-Host "  Skipped (too small): $FilePath" -ForegroundColor Yellow
            return
        }
        
        # For shell scripts, preserve shebang line
        if ($FileType -eq "shell" -and $content.StartsWith("#!/")) {
            $lines = $content -split "`n", 2
            $shebang = $lines[0]
            $rest = if ($lines.Length -gt 1) { $lines[1] } else { "" }
            $newContent = $shebang + "`n" + $Header + $rest
        }
        # For XML files, preserve XML declaration
        elseif ($FileType -eq "xml" -and $content -match "^\s*<\?xml") {
            $lines = $content -split "`n"
            $xmlDeclaration = $lines[0]
            $rest = ($lines[1..($lines.Length-1)] -join "`n")
            $newContent = $xmlDeclaration + "`n" + $Header + $rest
        }
        else {
            $newContent = $Header + $content
        }
        
        # Write the updated content
        Set-Content -Path $FilePath -Value $newContent -Encoding UTF8
        $script:filesProcessed++
        Write-Host "  Protected: $FilePath" -ForegroundColor Green
        
    } catch {
        Write-Host "  Error processing $FilePath : $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Process The Cathedral - Highest Priority
Write-Host ""
Write-Host "Processing The Cathedral (Sacred Core)..." -ForegroundColor Magenta

# Process the actual alden_core directory structure
if (Test-Path "alden_core") {
    # Python files in alden_core (main directory)
    Get-ChildItem -Path "alden_core" -Include "*.py" -File | ForEach-Object {
        Add-HeaderToFile -FilePath $_.FullName -Header $pythonHeader -FileType "python"
    }
    
    # Python files in alden_core/alden_cli (core CLI components)
    Get-ChildItem -Path "alden_core/alden_cli" -Recurse -Include "*.py" -File | ForEach-Object {
        Add-HeaderToFile -FilePath $_.FullName -Header $pythonHeader -FileType "python"
    }
    
    # Shell scripts in alden_core
    Get-ChildItem -Path "alden_core" -Recurse -Include "*.sh" -File | ForEach-Object {
        Add-HeaderToFile -FilePath $_.FullName -Header $shellHeader -FileType "shell"
    }
} else {
    Write-Host "  Warning: alden_core directory not found" -ForegroundColor Yellow
}

# Process Server Backend
Write-Host ""
Write-Host "Processing Server Backend..." -ForegroundColor Blue

if (Test-Path "server") {
    Get-ChildItem -Path "server" -Recurse -Include "*.py" -File | ForEach-Object {
        Add-HeaderToFile -FilePath $_.FullName -Header $pythonHeader -FileType "python"
    }
} else {
    Write-Host "  Warning: Server directory not found" -ForegroundColor Yellow
}

# Process Web Client
Write-Host ""
Write-Host "Processing Web Client..." -ForegroundColor Blue

if (Test-Path "web-client") {
    # JavaScript/TypeScript files
    Get-ChildItem -Path "web-client" -Recurse -Include "*.js","*.jsx","*.ts","*.tsx" -File | ForEach-Object {
        Add-HeaderToFile -FilePath $_.FullName -Header $jsHeader -FileType "javascript"
    }
    
    # HTML files
    Get-ChildItem -Path "web-client" -Recurse -Include "*.html" -File | ForEach-Object {
        Add-HeaderToFile -FilePath $_.FullName -Header $xmlHeader -FileType "xml"
    }
} else {
    Write-Host "  Warning: Web-client directory not found" -ForegroundColor Yellow
}

# Process Mobile Apps
Write-Host ""
Write-Host "Processing Mobile Applications..." -ForegroundColor Blue

if (Test-Path "mobile") {
    # Java/Kotlin files
    Get-ChildItem -Path "mobile" -Recurse -Include "*.java","*.kt" -File | ForEach-Object {
        Add-HeaderToFile -FilePath $_.FullName -Header $jsHeader -FileType "java"
    }
    
    # XML files (but exclude generated/build directories)
    Get-ChildItem -Path "mobile" -Recurse -Include "*.xml" -File | ForEach-Object {
        Add-HeaderToFile -FilePath $_.FullName -Header $xmlHeader -FileType "xml"
    }
} else {
    Write-Host "  Warning: Mobile directory not found" -ForegroundColor Yellow
}

# Process Agents
Write-Host ""
Write-Host "Processing AI Agents..." -ForegroundColor Blue

if (Test-Path "agents") {
    Get-ChildItem -Path "agents" -Recurse -Include "*.py" -File | ForEach-Object {
        Add-HeaderToFile -FilePath $_.FullName -Header $pythonHeader -FileType "python"
    }
} else {
    Write-Host "  Warning: Agents directory not found" -ForegroundColor Yellow
}

# Process root configuration files
Write-Host ""
Write-Host "Processing Root Configuration Files..." -ForegroundColor Blue

# Shell scripts in root
Get-ChildItem -Path "." -Include "*.sh" -File | ForEach-Object {
    Add-HeaderToFile -FilePath $_.FullName -Header $shellHeader -FileType "shell"
}

# PowerShell scripts in root (exclude header scripts to avoid circular issues)
Get-ChildItem -Path "." -Include "*.ps1" -File | Where-Object { 
    $_.Name -notlike "*glyphware*" -and $_.Name -notlike "*header*" 
} | ForEach-Object {
    Add-HeaderToFile -FilePath $_.FullName -Header $pythonHeader -FileType "powershell"
}

# Final Summary
Write-Host ""
Write-Host "Glyphware License Protection Complete!" -ForegroundColor Green
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  Files Protected: $filesProcessed" -ForegroundColor Green
Write-Host "  Files Skipped/Excluded: $filesSkipped" -ForegroundColor Yellow

Write-Host ""
Write-Host "Exclusions Applied:" -ForegroundColor Magenta
Write-Host "  - Virtual environments (.venv, venv)" -ForegroundColor White
Write-Host "  - Node.js dependencies (node_modules)" -ForegroundColor White
Write-Host "  - Python packages (site-packages)" -ForegroundColor White
Write-Host "  - Build directories (build, dist, target)" -ForegroundColor White
Write-Host "  - IDE/editor files (.vscode, .idea)" -ForegroundColor White

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Magenta
Write-Host "  1. Review the LICENSE-GLYPHWARE.md file" -ForegroundColor White
Write-Host "  2. Update README.md files with license information" -ForegroundColor White
Write-Host "  3. Commit changes to repository" -ForegroundColor White
Write-Host "  4. Consider legal review within 30 days" -ForegroundColor White

Write-Host ""
Write-Host "The Cathedral is now protected under Glyphware License v1.0" -ForegroundColor Cyan
Write-Host "Only source code files processed - dependencies excluded!" -ForegroundColor Green 