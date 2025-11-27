#!/usr/bin/env python3
"""
Replace header and footer properly with path adjustments
"""

import os
import re
from pathlib import Path

def extract_header_footer(source_file):
    """Extract header and footer"""
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        header_match = re.search(r'(<header[^>]*>.*?</header>)', content, re.DOTALL)
        header = header_match.group(1) if header_match else None
        
        footer_match = re.search(r'(<footer[^>]*>.*?</footer>)', content, re.DOTALL)
        footer = footer_match.group(1) if footer_match else None
        
        return header, footer
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def adjust_paths_for_depth(content, depth):
    """Adjust relative paths based on directory depth"""
    # depth 2 means /resources/page/ so we need ../../
    prefix = '../' * depth
    
    # Fix href paths
    content = re.sub(r'href="(?!http|#|mailto)([^"]+)"', f'href="{prefix}\\1"', content)
    # Fix src paths  
    content = re.sub(r'src="(?!http|data:)([^"]+)"', f'src="{prefix}\\1"', content)
    
    return content

def replace_header_footer(target_file, header, footer, depth):
    """Replace and adjust paths"""
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Adjust paths in header and footer
        adjusted_header = adjust_paths_for_depth(header, depth) if header else None
        adjusted_footer = adjust_paths_for_depth(footer, depth) if footer else None
        
        # Replace
        if adjusted_header:
            content = re.sub(r'<header[^>]*>.*?</header>', adjusted_header, content, flags=re.DOTALL)
        
        if adjusted_footer:
            content = re.sub(r'<footer[^>]*>.*?</footer>', adjusted_footer, content, flags=re.DOTALL)
        
        if content != original:
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

source = 'PumaPulse.rocks/index.html'

targets = [
    ('PumaPulse.rocks/resources/marketing-archetype-quiz/index.html', 2),
    ('PumaPulse.rocks/resources/website-improvement-plan/index.html', 2),
]

print("🔧 FIXING HEADER/FOOTER WITH PATH ADJUSTMENT...\n")

header, footer = extract_header_footer(source)

if header and footer:
    print("✓ Extracted from source\n")
    
    for target_file, depth in targets:
        if Path(target_file).exists():
            if replace_header_footer(target_file, header, footer, depth):
                print(f"✓ Fixed: {target_file} (depth={depth})")
        else:
            print(f"❌ Not found: {target_file}")
else:
    print("❌ Failed to extract")

print("\n✅ DONE!")
