#!/usr/bin/env python3
"""
Replace broken header and footer with correct ones from index.html
"""

import os
import re
from pathlib import Path

def extract_header_footer(source_file):
    """Extract header and footer from source file"""
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract header (from <header to </header>)
        header_match = re.search(r'(<header[^>]*>.*?</header>)', content, re.DOTALL)
        header = header_match.group(1) if header_match else None
        
        # Extract footer (from <footer to </footer>)
        footer_match = re.search(r'(<footer[^>]*>.*?</footer>)', content, re.DOTALL)
        footer = footer_match.group(1) if footer_match else None
        
        return header, footer
    except Exception as e:
        print(f"Error extracting from {source_file}: {e}")
        return None, None

def replace_header_footer(target_file, header, footer):
    """Replace header and footer in target file"""
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace header
        if header:
            content = re.sub(r'<header[^>]*>.*?</header>', header, content, flags=re.DOTALL)
        
        # Replace footer
        if footer:
            content = re.sub(r'<footer[^>]*>.*?</footer>', footer, content, flags=re.DOTALL)
        
        if content != original_content:
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"Error replacing in {target_file}: {e}")
        return False

# Source file with correct header/footer
source_file = 'PumaPulse.rocks/index.html'

# Target files with broken header/footer
target_files = [
    'PumaPulse.rocks/resources/marketing-archetype-quiz/index.html',
    'PumaPulse.rocks/resources/website-improvement-plan/index.html',
]

print("🔧 FIXING HEADER AND FOOTER...\n")
print(f"Source: {source_file}\n")

# Extract header and footer
header, footer = extract_header_footer(source_file)

if header and footer:
    print("✓ Extracted header and footer\n")
    
    for target_file in target_files:
        if Path(target_file).exists():
            if replace_header_footer(target_file, header, footer):
                print(f"✓ Fixed: {target_file}")
            else:
                print(f"  No changes: {target_file}")
        else:
            print(f"❌ Not found: {target_file}")
else:
    print("❌ Failed to extract header/footer")

print("\n✅ DONE!")
print("Header and footer replaced, content unchanged.")
