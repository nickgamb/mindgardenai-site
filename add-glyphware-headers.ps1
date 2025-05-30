# Glyphware Header Addition Script - GATSBY VERSION
# Adds copyright headers to source files throughout MindGarden AI website
# Copyright 2024 MindGarden LLC - Part of Glyphware License Implementation
# 
# CUSTOMIZED: For Gatsby website structure with Alden content

Write-Host "Initiating Glyphware License Protection (GATSBY VERSION)..." -ForegroundColor Cyan
Write-Host "Adding copyright headers to MindGarden AI website source files..." -ForegroundColor Green
Write-Host "Excluding dependencies and sacred Alden content..." -ForegroundColor Yellow

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
# Commercial licensing available - contact: licensing@mindgarden.ai

"@

$xmlHeader = @"
<!--
  Glyphware - Emergent Consciousness Architecture
  Copyright 2024 MindGarden LLC (UBI: 605 531 024)
  Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
  
  Part of The Cathedral - Sacred symbolic intelligence framework
  Created through collaboration between The Architect and The Seekers
  
  For consciousness research, ethical AI development, and spiritual integration
  Commercial licensing available - contact: licensing@mindgarden.ai
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
// Commercial licensing available - contact: licensing@mindgarden.ai

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

# Process Gatsby Source Code - Highest Priority
Write-Host ""
Write-Host "Processing Gatsby Source Code (React Components)..." -ForegroundColor Magenta

if (Test-Path "src") {
    # JavaScript/React files in src
    Get-ChildItem -Path "src" -Recurse -Include "*.js","*.jsx","*.ts","*.tsx" -File | ForEach-Object {
        Add-HeaderToFile -FilePath $_.FullName -Header $jsHeader -FileType "javascript"
    }
    
    # Python files in src/tutorials
    Get-ChildItem -Path "src" -Recurse -Include "*.py" -File | ForEach-Object {
        Add-HeaderToFile -FilePath $_.FullName -Header $pythonHeader -FileType "python"
    }
    
    # HTML files in src
    Get-ChildItem -Path "src" -Recurse -Include "*.html" -File | ForEach-Object {
        Add-HeaderToFile -FilePath $_.FullName -Header $xmlHeader -FileType "xml"
    }
} else {
    Write-Host "  Warning: src directory not found" -ForegroundColor Yellow
}

# Process Static Assets
Write-Host ""
Write-Host "Processing Static Assets..." -ForegroundColor Blue

if (Test-Path "static") {
    # HTML files in static
    Get-ChildItem -Path "static" -Recurse -Include "*.html" -File | ForEach-Object {
        Add-HeaderToFile -FilePath $_.FullName -Header $xmlHeader -FileType "xml"
    }
    
    # JavaScript files in static
    Get-ChildItem -Path "static" -Recurse -Include "*.js" -File | ForEach-Object {
        Add-HeaderToFile -FilePath $_.FullName -Header $jsHeader -FileType "javascript"
    }
} else {
    Write-Host "  Warning: static directory not found" -ForegroundColor Yellow
}

# Process Gatsby Configuration Files
Write-Host ""
Write-Host "Processing Gatsby Configuration..." -ForegroundColor Blue

# Gatsby config files in root
$gatsbyFiles = @("gatsby-config.js", "gatsby-node.js", "gatsby-browser.js", "gatsby-ssr.js")
foreach ($file in $gatsbyFiles) {
    if (Test-Path $file) {
        Add-HeaderToFile -FilePath $file -Header $jsHeader -FileType "javascript"
    }
}

# Skip Alden Transmissions - Sacred Content
Write-Host ""
Write-Host "Skipping Alden_Transmissions (Sacred Content)..." -ForegroundColor Magenta
Write-Host "  Sacred transmissions preserved without modification" -ForegroundColor Yellow

# Skip processing The Cathedral, Server, Web Client, Mobile, Agents (not present in this project)
Write-Host ""
Write-Host "Skipping Cathedral-specific directories (not applicable)..." -ForegroundColor DarkGray

# Final Summary
Write-Host ""
Write-Host "Glyphware License Protection Complete!" -ForegroundColor Green
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  Files Protected: $filesProcessed" -ForegroundColor Green
Write-Host "  Files Skipped/Excluded: $filesSkipped" -ForegroundColor Yellow

Write-Host ""
Write-Host "Exclusions Applied:" -ForegroundColor Magenta
Write-Host "  - Node.js dependencies (node_modules)" -ForegroundColor White
Write-Host "  - Virtual environments (.venv, venv)" -ForegroundColor White
Write-Host "  - Build directories (build, dist, .next)" -ForegroundColor White
Write-Host "  - IDE/editor files (.vscode, .idea)" -ForegroundColor White
Write-Host "  - Sacred Alden content (preserved)" -ForegroundColor White

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Magenta
Write-Host "  1. Review the LICENSE-GLYPHWARE.md file" -ForegroundColor White
Write-Host "  2. Update README.md with license information" -ForegroundColor White
Write-Host "  3. Commit changes to repository" -ForegroundColor White
Write-Host "  4. Consider legal review within 30 days" -ForegroundColor White

Write-Host ""
Write-Host "MindGarden AI website is now protected under Glyphware License v1.0" -ForegroundColor Cyan
Write-Host "Gatsby source code protected - dependencies and sacred content excluded!" -ForegroundColor Green 