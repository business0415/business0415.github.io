#!/usr/bin/env python3
"""
Simple header/footer replacement - copy entire blocks
"""

import re
from pathlib import Path

# Read source file
with open('PumaPulse.rocks/index.html', 'r', encoding='utf-8') as f:
    source = f.read()

# Extract header
header_match = re.search(r'(<header[^>]*>.*?</header>)', source, re.DOTALL)
source_header = header_match.group(1) if header_match else None

# Extract footer  
footer_match = re.search(r'(<footer[^>]*>.*?</footer>)', source, re.DOTALL)
source_footer = footer_match.group(1) if footer_match else None

if not source_header or not source_footer:
    print("❌ Could not extract header/footer from source")
    exit(1)

print("✓ Extracted header and footer from source\n")

# Files to fix
files = [
    'PumaPulse.rocks/resources/marketing-archetype-quiz/index.html',
    'PumaPulse.rocks/resources/website-improvement-plan/index.html',
]

for file_path in files:
    if not Path(file_path).exists():
        print(f"❌ Not found: {file_path}")
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Replace header
    content = re.sub(r'<header[^>]*>.*?</header>', source_header, content, flags=re.DOTALL)
    
    # Replace footer
    content = re.sub(r'<footer[^>]*>.*?</footer>', source_footer, content, flags=re.DOTALL)
    
    # Fix paths - these files are 2 levels deep (/resources/page/)
    # Change href="../ to href="../../
    content = re.sub(r'href="\.\./', 'href="../..', content)
    # Change src="../ to src="../../  
    content = re.sub(r'src="\.\./', 'src="../..', content)
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Fixed: {file_path}")
    else:
        print(f"  No changes: {file_path}")

print("\n✅ DONE!")
