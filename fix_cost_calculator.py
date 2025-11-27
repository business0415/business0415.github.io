#!/usr/bin/env python3
"""
Fix website-cost-calculator header and footer
"""

import re
from pathlib import Path

# Read correct header and footer from resources/index.html
with open('PumaPulse.rocks/resources/index.html', 'r', encoding='utf-8') as f:
    source = f.read()

# Extract header
header_match = re.search(r'(<header[^>]*class="[^"]*fl-builder-content[^"]*"[^>]*>.*?</header>)', source, re.DOTALL)
correct_header = header_match.group(1) if header_match else None

# Extract footer
footer_match = re.search(r'(<footer[^>]*class="[^"]*fl-builder-content[^"]*"[^>]*>.*?</footer>)', source, re.DOTALL)
correct_footer = footer_match.group(1) if footer_match else None

if not correct_header or not correct_footer:
    print("❌ Could not extract header/footer")
    exit(1)

print("✓ Extracted header and footer\n")

# Adjust paths (same depth as resources/index.html)
correct_header = correct_header.replace('href="../', 'href="../../')
correct_header = correct_header.replace('src="../', 'src="../../')

correct_footer = correct_footer.replace('href="../', 'href="../../')
correct_footer = correct_footer.replace('src="../', 'src="../../')

file_path = 'PumaPulse.rocks/resources/website-cost-calculator/index.html'

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

# Replace footer
content = re.sub(
    r'<footer[^>]*class="[^"]*fl-builder-content[^"]*"[^>]*>.*?</footer>',
    correct_footer,
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
print("Header and footer replaced.")
