#!/usr/bin/env python3
"""
Fix header navigation URLs in the 3 resource pages
"""

import re
from pathlib import Path

files = [
    'PumaPulse.rocks/resources/marketing-archetype-quiz/index.html',
    'PumaPulse.rocks/resources/website-improvement-plan/index.html',
    'PumaPulse.rocks/resources/website-cost-calculator/index.html',
]

print("🔧 FIXING HEADER NAVIGATION URLS...\n")

for file_path in files:
    if not Path(file_path).exists():
        print(f"❌ Not found: {file_path}")
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix Services link
    content = re.sub(
        r'(<a title="Services" href=")\.\./(index\.html">)',
        r'\1../../services/\2',
        content
    )
    
    # Fix home/logo links
    content = re.sub(
        r'href="index\.html"',
        'href="../../index.html"',
        content
    )
    
    # Fix any remaining single ../ that should be ../../
    # But be careful not to break already correct paths
    content = re.sub(
        r'href="\.\./(?!\.\.)',
        'href="../../',
        content
    )
    
    content = re.sub(
        r'src="\.\./(?!\.\.)',
        'src="../../',
        content
    )
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Fixed: {file_path}")
    else:
        print(f"  No changes: {file_path}")

print("\n✅ DONE!")
print("All header URLs corrected for proper depth.")
