#!/usr/bin/env python3
"""
Replace the incomplete header in website-improvement-plan with correct one
"""

import re
from pathlib import Path

# Read the correct header from resources/index.html
with open('PumaPulse.rocks/resources/index.html', 'r', encoding='utf-8') as f:
    source = f.read()

# Extract header
header_match = re.search(r'(<header[^>]*class="[^"]*fl-builder-content[^"]*"[^>]*>.*?</header>)', source, re.DOTALL)
correct_header = header_match.group(1) if header_match else None

if not correct_header:
    print("❌ Could not extract header")
    exit(1)

print("✓ Extracted correct header\n")

# Adjust paths for this file (it's at /resources/page/ so needs ../ instead of ../../)
# Actually it needs the same depth as resources/index.html
correct_header = correct_header.replace('href="../', 'href="../../')
correct_header = correct_header.replace('src="../', 'src="../../')

file_path = 'PumaPulse.rocks/resources/website-improvement-plan/index.html'

if not Path(file_path).exists():
    print(f"❌ Not found: {file_path}")
    exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# Replace header
content = re.sub(
    r'<header[^>]*class="[^"]*fl-builder-content[^"]*"[^>]*>.*?</header>',
    correct_header,
    content,
    flags=re.DOTALL
)

if content != original:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Fixed: {file_path}")
else:
    print(f"  No changes: {file_path}")

print("\n✅ DONE!")
print("Header replaced with complete navigation.")
