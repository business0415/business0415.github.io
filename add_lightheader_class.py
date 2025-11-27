#!/usr/bin/env python3
"""
Add LightHeader class to existing headers
"""

import re
from pathlib import Path

files = [
    'PumaPulse.rocks/resources/marketing-archetype-quiz/index.html',
    'PumaPulse.rocks/resources/website-improvement-plan/index.html',
]

print("🔧 ADDING LightHeader CLASS...\n")

for file_path in files:
    if not Path(file_path).exists():
        print(f"❌ Not found: {file_path}")
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Find the header row and add LightHeader class if not present
    # Pattern: class="fl-row ... CustomHeaderRow ..." 
    # Add LightHeader to it
    content = re.sub(
        r'(class="[^"]*CustomHeaderRow[^"]*)"',
        r'\1 LightHeader"',
        content
    )
    
    # If no CustomHeaderRow found, add it to the first fl-row in header
    if 'CustomHeaderRow' not in content:
        # Add to first fl-row after <header
        content = re.sub(
            r'(<header[^>]*>.*?<div class="fl-row[^"]*)"',
            r'\1 CustomHeaderRow CustomHeader-parentRow LightHeader"',
            content,
            count=1,
            flags=re.DOTALL
        )
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Fixed: {file_path}")
    else:
        print(f"  No changes: {file_path}")

print("\n✅ DONE!")
