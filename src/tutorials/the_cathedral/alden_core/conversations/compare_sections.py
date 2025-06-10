import os
import json
from pathlib import Path
import difflib
from typing import List, Dict, Set

def read_file_content(filepath: str) -> str:
    """Read and normalize file content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        # Normalize content: lowercase, remove extra whitespace
        return ' '.join(content.lower().split())
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return ""

def get_all_files(directory: str) -> Dict[str, str]:
    """Get all files in directory and subdirectories."""
    files = {}
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.txt') or filename.endswith('.md'):
                full_path = os.path.join(root, filename)
                files[full_path] = read_file_content(full_path)
    return files

def find_similar_files(parsed_files: Dict[str, str], alden_files: Dict[str, str], 
                      similarity_threshold: float = 0.8) -> Dict[str, List[str]]:
    """Find similar files between the two directories using content similarity."""
    similar_files = {}
    unmatched_files = set(parsed_files.keys())
    
    for parsed_path, parsed_content in parsed_files.items():
        if not parsed_content:  # Skip empty files
            continue
            
        best_match = None
        best_score = 0
        
        for alden_path, alden_content in alden_files.items():
            if not alden_content:  # Skip empty files
                continue
                
            # Calculate similarity ratio between contents
            score = difflib.SequenceMatcher(None, parsed_content, alden_content).ratio()
            if score > best_score and score >= similarity_threshold:
                best_score = score
                best_match = alden_path
        
        if best_match:
            similar_files[parsed_path] = best_match
            unmatched_files.remove(parsed_path)
    
    return similar_files, unmatched_files

def main():
    # Define directories
    parsed_dir = "parsed_sections"
    alden_dir = "Alden_Transmissions"
    
    print("Reading files from parsed_sections...")
    parsed_files = get_all_files(parsed_dir)
    print(f"Found {len(parsed_files)} files in parsed_sections")
    
    print("\nReading files from Alden_Transmissions...")
    alden_files = get_all_files(alden_dir)
    print(f"Found {len(alden_files)} files in Alden_Transmissions")
    
    print("\nComparing file contents...")
    similar_files, unmatched_files = find_similar_files(parsed_files, alden_files)
    
    # Print results
    print("\n=== Files with Similar Content ===")
    for parsed_path, alden_path in similar_files.items():
        print(f"\nParsed: {parsed_path}")
        print(f"Alden:  {alden_path}")
    
    print("\n=== Files Only in Parsed Sections ===")
    for unmatched_path in unmatched_files:
        print(f"\n{unmatched_path}")
    
    # Save results to JSON
    results = {
        "similar_files": {str(k): str(v) for k, v in similar_files.items()},
        "unique_files": [str(path) for path in unmatched_files]
    }
    
    with open("section_comparison_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to section_comparison_results.json")

if __name__ == "__main__":
    main() 