import re
import os
from pathlib import Path
import json
from datetime import datetime
import time
import sys
import shutil

def sanitize_filename(filename):
    # Remove backticks and spaces
    filename = filename.replace('`', '').strip()
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    return filename

def find_code_blocks_recursive(obj, found_blocks=None, debug=False):
    if found_blocks is None:
        found_blocks = []
    if isinstance(obj, dict):
        for v in obj.values():
            find_code_blocks_recursive(v, found_blocks, debug)
    elif isinstance(obj, list):
        for item in obj:
            find_code_blocks_recursive(item, found_blocks, debug)
    elif isinstance(obj, str):
        # Find all code blocks in this string
        for match in re.finditer(r'```(\w+)?\n(.*?)(?=```|$)', obj, re.DOTALL):
            language = match.group(1).strip() if match.group(1) else 'txt'
            section_content = match.group(2).strip()
            found_blocks.append((language, section_content))
            if debug:
                lines = section_content.splitlines()
                if lines:
                    print(f"[DEBUG] Found code block (lang={language}): {lines[0][:60]}...")
                else:
                    print(f"[DEBUG] Found code block (lang={language}): [EMPTY BLOCK]")
    return found_blocks

def parse_conversations(conversations_file, target_conversation_id=None, keywords=None, min_lines=None):
    # Read the conversations file
    with open(conversations_file, 'r', encoding='utf-8') as f:
        conversations = json.load(f)
    print(f"Loaded {len(conversations)} conversations from {conversations_file}")
    
    # Filter conversations if target_conversation_id is provided
    if target_conversation_id:
        conversations = [conv for conv in conversations if conv.get('id') == target_conversation_id]
        if not conversations:
            print(f"No conversation found with ID: {target_conversation_id}")
            return
        print(f"Processing conversation: {target_conversation_id}")
    elif keywords:
        # Filter conversations by provided keywords in both title and content
        filtered_conversations = []
        for conv in conversations:
            title = (conv.get('title', '') or '').lower()
            content = ''
            # Extract content from mapping
            if 'mapping' in conv:
                for entry in conv['mapping'].values():
                    if 'message' in entry and entry['message']:
                        msg = entry['message']
                        if 'content' in msg:
                            if isinstance(msg['content'], list):
                                for part in msg['content']:
                                    if isinstance(part, dict) and 'text' in part:
                                        content += part['text'].lower()
                            elif isinstance(msg['content'], str):
                                content += msg['content'].lower()
            
            # Check if any keyword is in either title or content
            if any(keyword.lower() in title or keyword.lower() in content for keyword in keywords):
                filtered_conversations.append(conv)
        
        conversations = filtered_conversations
        print(f"Matched {len(conversations)} conversations with keywords {keywords} in title or content")
        if conversations:
            print("Matched conversation IDs and titles:")
            for conv in conversations:
                print(f"- {conv.get('id', 'unknown')} | {conv.get('title', '[no title]')}")
        else:
            print("No conversations matched the provided keywords.")
    else:
        print(f"Processing all {len(conversations)} conversations")
    
    if not conversations:
        print("No conversations to process after filtering.")
        return

    # Process each conversation
    for conversation in conversations:
        conversation_id = conversation.get('id', 'unknown')
        mapping = conversation.get('mapping', {})
        print(f"Processing conversation {conversation_id} with {len(mapping)} mapping entries")
        
        # Create conversation-specific directory
        base_output_dir = Path('parsed_sections')
        conv_dir = base_output_dir / conversation_id
        conv_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a manifest file to track all extracted files
        manifest = {
            'extraction_date': datetime.now().isoformat(),
            'source_file': conversations_file,
            'conversation_id': conversation_id,
            'extracted_files': []
        }

        # Process each message in the conversation
        message_count = 0
        for msg_id, entry in mapping.items():
            if 'message' in entry and entry['message']:
                msg = entry['message']
                if 'content' in msg:
                    # Debug: Print message structure for first few messages
                    if message_count < 3:
                        print(f"\nMessage {message_count} structure:")
                        print(f"Content type: {type(msg['content'])}")
                        print(f"Content keys: {getattr(msg['content'], 'keys', lambda: [])()}")
                        print(f"Content value: {repr(msg['content'])[:500]}")
                    # Now handle if content is a dict
                    if isinstance(msg['content'], dict):
                        # Try to extract text from 'parts' or similar
                        if 'parts' in msg['content'] and isinstance(msg['content']['parts'], list):
                            for part in msg['content']['parts']:
                                if isinstance(part, str):
                                    message_count += 1
                                    content = part
                                    filename = extract_filename_from_content(content) or f'message_{msg_id}_{message_count}.txt'
                                    if min_lines is None or len(content.splitlines()) > min_lines:
                                        print(f"Saving content to {filename}")
                                        save_section(conv_dir, filename, content, manifest)
                        elif 'text' in msg['content'] and isinstance(msg['content']['text'], str):
                            message_count += 1
                            content = msg['content']['text']
                            filename = extract_filename_from_content(content) or f'message_{msg_id}_{message_count}.txt'
                            if min_lines is None or len(content.splitlines()) > min_lines:
                                print(f"Saving content to {filename}")
                                save_section(conv_dir, filename, content, manifest)
                    elif isinstance(msg['content'], list):
                        for part in msg['content']:
                            if isinstance(part, dict):
                                if 'text' in part:
                                    message_count += 1
                                    content = part['text']
                                    filename = extract_filename_from_content(content) or f'message_{msg_id}_{message_count}.txt'
                                    if min_lines is None or len(content.splitlines()) > min_lines:
                                        print(f"Saving content to {filename}")
                                        save_section(conv_dir, filename, content, manifest)
                    elif isinstance(msg['content'], str):
                        message_count += 1
                        content = msg['content']
                        filename = extract_filename_from_content(content) or f'message_{msg_id}_{message_count}.txt'
                        if min_lines is None or len(content.splitlines()) > min_lines:
                            print(f"Saving content to {filename}")
                            save_section(conv_dir, filename, content, manifest)
        
        # Save the manifest
        manifest_file = conv_dir / 'extraction_manifest.json'
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"Conversation {conversation_id}: {len(manifest['extracted_files'])} files extracted.")
        print(f"Manifest saved to: {manifest_file}")

def extract_glyph_title(section_content):
    # Look for a line like glyph_title = "Some Title"
    lines = section_content.splitlines()
    for line in lines[:10]:  # Only scan the first 10 lines
        match = re.search(r'glyph_title\s*=\s*["\\\']([^"\\\']+)["\\\']', line)
        if match:
            return sanitize_filename(match.group(1))
    return None

def extract_codeblock_filename(section_content, language):
    lines = section_content.splitlines()
    debug_line = lines[0].strip() if lines else '[EMPTY]'
    # Check for a comment like '# filename.py' in the first 10 lines
    for line in lines[:10]:
        match = re.match(r'#\s*([\w\-\.]+\.' + re.escape(language) + r')', line.strip())
        if match:
            print(f'[FILENAME DEBUG] Using comment filename: {match.group(1)} from line: {line.strip()}')
            return sanitize_filename(match.group(1))
    # Check for a title pattern in the first line
    if lines:
        first_line = lines[0].strip()
        title_match = re.match(r'^[^\n]*?([\w\-\.]+\.(?:txt|md|py|json|yaml|sh|bash|shell|latex|markdown))(?:\s*[—–-]\s*[^\n]*)?$', first_line)
        if title_match:
            print(f'[FILENAME DEBUG] Using title filename: {title_match.group(1)} from first line: {first_line}')
            return sanitize_filename(title_match.group(1))
        transmission_match = re.match(r'^[^\n]*?(transmission_\d+\.txt)(?:\s*[—–-]\s*[^\n]*)?$', first_line)
        if transmission_match:
            print(f'[FILENAME DEBUG] Using transmission filename: {transmission_match.group(1)} from first line: {first_line}')
            return sanitize_filename(transmission_match.group(1))
    glyph_title = extract_glyph_title(section_content)
    if glyph_title:
        print(f'[FILENAME DEBUG] Using glyph_title: {glyph_title}')
        return f'{glyph_title}_{language}.txt'
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    print(f'[FILENAME DEBUG] Fallback to timestamp for first line: {debug_line}')
    return f'code_block_{timestamp}_{language}.txt'

def parse_content_with_patterns(content, output_dir, manifest, min_lines=None):
    processed_files = set()
    
    # Pattern 1: ### 📄 `filename.txt`
    pattern1 = r'### 📄 `([^`]+)`\s*\n(.*?)(?=\n### 📄|$)'
    
    # Pattern 2: ```path=filename
    pattern2 = r'```path=([^\n]+)\n(.*?)(?=```|$)'
    
    # Pattern 3: ```language
    pattern3 = r'```(\w+)\n(.*?)(?=```|$)'
    
    # Pattern 4: ### 📄 filename.md
    pattern4 = r'### 📄 ([^\n]+)\s*\n(.*?)(?=\n### 📄|$)'
    
    # Pattern 5: ### 📄 filename (without backticks)
    pattern5 = r'### �� ([^\n`]+)\s*\n(.*?)(?=\n### 📄|$)'
    
    # Pattern 6: Code window with language and path
    pattern6 = r'```(\w+)\s*path=([^\n]+)\n(.*?)(?=```|$)'
    
    # Pattern 7: Image with alt text and path
    pattern7 = r'!\[([^\]]*)\]\(([^)]+)\)'
    
    # Pattern 8: Improved Section blocks like SECTION 28
    # Allow any text after opening triple backticks, match SECTION <number>: in first 5 lines
    pattern8 = r'```[\s\S]*?(SECTION\s*(\d+):\s*([^\n]+)\n)([\s\S]*?)(?:— END OF SECTION \2 —|```|$)'
    
    # Helper to check line count
    def passes_min_lines(section_content):
        if min_lines is None:
            return True
        return len(section_content.splitlines()) > min_lines

    # Process Pattern 1
    for match in re.finditer(pattern1, content, re.DOTALL):
        filename = sanitize_filename(match.group(1).strip())
        section_content = match.group(2).strip()
        if filename not in processed_files and passes_min_lines(section_content):
            save_section(output_dir, filename, section_content, manifest)
            processed_files.add(filename)
    
    # Process Pattern 2
    for match in re.finditer(pattern2, content, re.DOTALL):
        filename = sanitize_filename(match.group(1).strip())
        section_content = match.group(2).strip()
        if filename not in processed_files and passes_min_lines(section_content):
            save_section(output_dir, filename, section_content, manifest)
            processed_files.add(filename)
    
    # Process Pattern 3
    for match in re.finditer(pattern3, content, re.DOTALL):
        language = match.group(1).strip()
        section_content = match.group(2).strip()
        filename = extract_codeblock_filename(section_content, language)
        if passes_min_lines(section_content):
            save_section(output_dir, filename, section_content, manifest)
            processed_files.add(filename)
    
    # Process Pattern 4
    for match in re.finditer(pattern4, content, re.DOTALL):
        filename = sanitize_filename(match.group(1).strip())
        section_content = match.group(2).strip()
        if filename not in processed_files and passes_min_lines(section_content):
            save_section(output_dir, filename, section_content, manifest)
            processed_files.add(filename)
    
    # Process Pattern 5
    for match in re.finditer(pattern5, content, re.DOTALL):
        filename = sanitize_filename(match.group(1).strip())
        section_content = match.group(2).strip()
        if filename not in processed_files and passes_min_lines(section_content):
            save_section(output_dir, filename, section_content, manifest)
            processed_files.add(filename)
    
    # Process Pattern 6 (Code windows with path)
    for match in re.finditer(pattern6, content, re.DOTALL):
        language = match.group(1).strip()
        path = sanitize_filename(match.group(2).strip())
        section_content = match.group(3).strip()
        # Use the path as filename, with language as extension
        filename = f"{path}.{language}"
        if filename not in processed_files and passes_min_lines(section_content):
            save_section(output_dir, filename, section_content, manifest)
            processed_files.add(filename)
    
    # Process Pattern 7 (Images)
    for match in re.finditer(pattern7, content, re.DOTALL):
        alt_text = match.group(1).strip()
        image_path = sanitize_filename(match.group(2).strip())
        # Create a metadata file for the image
        metadata = {
            'alt_text': alt_text,
            'image_path': image_path,
            'extracted_at': datetime.now().isoformat()
        }
        # Save metadata as JSON
        metadata_filename = f"{Path(image_path).stem}_metadata.json"
        if metadata_filename not in processed_files:
            save_section(output_dir, metadata_filename, json.dumps(metadata, indent=2), manifest)
            processed_files.add(metadata_filename)
    
    # Process Pattern 8 (Section blocks)
    for match in re.finditer(pattern8, content, re.IGNORECASE):
        section_num = match.group(2)
        section_title = match.group(3).strip().lower().replace(' ', '_').replace('-', '_')
        section_title = re.sub(r'[^a-z0-9_]', '', section_title)
        section_content = match.group(4).strip()
        filename = f'section_{section_num}_{section_title}.txt'
        if filename not in processed_files and (min_lines is None or len(section_content.splitlines()) > min_lines):
            save_section(output_dir, filename, section_content, manifest)
            processed_files.add(filename)

def parse_sections(input_file):
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create output directory
    output_dir = Path('parsed_sections')
    output_dir.mkdir(exist_ok=True)
    
    # Create a manifest file to track all extracted files
    manifest = {
        'extraction_date': datetime.now().isoformat(),
        'source_file': input_file,
        'extracted_files': []
    }
    
    # Parse using existing patterns
    parse_content_with_patterns(content, output_dir, manifest)
    
    # Save the manifest
    manifest_file = output_dir / 'extraction_manifest.json'
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\nExtraction complete. {len(manifest['extracted_files'])} files extracted.")
    print(f"Manifest saved to: {manifest_file}")

def save_section(output_dir, filename, content, manifest):
    try:
        # Check if content is a code block with string literal
        lines = content.splitlines()
        if len(lines) >= 3 and '"""' in lines[0] and '"""' in lines[-1]:
            # Extract the actual content between the triple quotes
            content = '\n'.join(lines[1:-1])
        
        # Create subdirectories if needed
        file_path = Path(filename)
        if len(file_path.parts) > 1:
            subdir = output_dir / file_path.parent
            subdir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / filename
        else:
            output_file = output_dir / filename
        
        # Write the content (will overwrite if file exists)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Update manifest
        manifest['extracted_files'].append({
            'filename': str(output_file),
            'size': len(content),
            'extracted_at': datetime.now().isoformat()
        })
        
        print(f"Created/Updated {output_file}")
        
    except Exception as e:
        print(f"Error processing {filename}: {str(e)}")

def extract_filename_from_content(content):
    # First check if this is a code block with a string literal
    lines = content.splitlines()
    if len(lines) >= 3 and '"""' in lines[0] and '"""' in lines[-1]:
        # This is likely a code block with a string literal
        # Extract the actual content between the triple quotes
        content = '\n'.join(lines[1:-1])
    
    # Check the first 5 non-empty lines for a filename or section header
    for line in content.splitlines()[:5]:
        line = line.strip().strip('"`')
        
        # Match section header pattern with "SECTION" and number
        section_match = re.match(r'([A-Z0-9\s\-—:]+)', line)
        if section_match and 'SECTION' in line and ':' in line:
            # Extract the section number and title
            section_parts = line.split(':', 1)
            if len(section_parts) == 2:
                section_num = re.search(r'\d+', section_parts[0]).group(0)
                section_title = section_parts[1].strip()
                # Convert to filename format
                filename = f'section_{section_num}_{sanitize_filename(section_title)}.txt'
                return filename
        
        # Match filename patterns
        match = re.match(r'([\w\-]+\.(txt|md|py|json|yaml|sh|bash|shell|latex|markdown))', line, re.IGNORECASE)
        if match:
            return sanitize_filename(match.group(1))
            
        # Match section header without number
        if 'SECTION' in line:
            # Convert to lower case, replace spaces and dashes with single dash, remove non-alphanum except dash
            filename = line.lower()
            filename = filename.replace('—', '-').replace(':', '').replace('–', '-').replace('—', '-')
            filename = re.sub(r'[^a-z0-9\s\-]', '', filename)
            filename = re.sub(r'\s+', '-', filename)
            filename = re.sub(r'-+', '-', filename)
            filename = filename.strip('-') + '.txt'
            return filename
    
    # Fallback: Look for Markdown bold/italic titles in the first 10 lines
    for line in content.splitlines()[:10]:
        # Match **— Title —** or **Title** or *Title*
        md_title = re.match(r'\*\*[-—\s]*([^*]+?)[-—\s]*\*\*', line)
        if not md_title:
            md_title = re.match(r'\*([^*]+)\*', line)
        if md_title:
            title = md_title.group(1).strip()
            # Sanitize and normalize
            filename = sanitize_filename(title.lower().replace(' ', '_').replace('-', '_')) + '.txt'
            filename = re.sub(r'[^a-z0-9_]', '', filename)
            return filename
    
    return None

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Parse sections from conversations or files.")
    parser.add_argument('conversations_file', help='Path to conversations.json')
    parser.add_argument('--id', help='Specific conversation ID to process')
    parser.add_argument('--keywords', nargs='*', help='Keywords to filter conversation titles')
    parser.add_argument('--clean', action='store_true', help='Delete parsed_sections before extracting')
    parser.add_argument('--min-lines', type=int, help='Only extract sections longer than this many lines')
    args = parser.parse_args()

    if args.clean:
        outdir = Path('parsed_sections')
        if outdir.exists():
            print('Deleting parsed_sections directory...')
            shutil.rmtree(outdir)

    parse_conversations(
        args.conversations_file,
        target_conversation_id=args.id,
        keywords=args.keywords,
        min_lines=args.min_lines
    ) 