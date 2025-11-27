#!/usr/bin/env python3
"""
Smart header/footer replacement - only replace the visible header/footer, not head section
"""

import re
from pathlib import Path

# Read source
with open('PumaPulse.rocks/index.html', 'r', encoding='utf-8') as f:
    source = f.read()

# Extract just the header element (after <body>)
header_match = re.search(r'(<header[^>]*class="[^"]*fl-builder-content[^"]*"[^>]*>.*?</header>)', source, re.DOTALL)
source_header = header_match.group(1) if header_match else None

# Extract footer
footer_match = re.search(r'(<footer[^>]*class="[^"]*fl-builder-content[^"]*"[^>]*>.*?</footer>)', source, re.DOTALL)
source_footer = footer_match.group(1) if footer_match else None

if not source_header or not source_footer:
    print("❌ Could not extract")
    exit(1)

print("✓ Extracted header and footer\n")

# Fix only the navigation links in header to be relative
# Change absolute paths to relative for 2-level depth
source_header = source_header.replace('href="services/', 'href="../../services/')
source_header = source_header.replace('href="case-studies/', 'href="../../case-studies/')
source_header = source_header.replace('href="about/', 'href="../../about/')
source_header = source_header.replace('href="resources/', 'href="../../resources/')
source_header = source_header.replace('href="index.html"', 'href="../../index.html"')

# Fix logo images
source_header = source_header.replace('src="wp-content/', 'src="../../wp-content/')

# Same for footer
source_footer = source_footer.replace('href="services/', 'href="../../services/')
source_footer = source_footer.replace('href="case-studies/', 'href="../../case-studies/')
source_footer = source_footer.replace('href="about/', 'href="../../about/')
source_footer = source_footer.replace('href="resources/', 'href="../../resources/')
source_footer = source_footer.replace('href="contact/', 'href="../../contact/')
source_footer = source_footer.replace('href="index.html"', 'href="../../index.html"')
source_footer = source_footer.replace('src="wp-content/', 'src="../../wp-content/')

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
    
    # Replace only the header element (not the <head> section)
    content = re.sub(
        r'<header[^>]*class="[^"]*fl-builder-content[^"]*"[^>]*>.*?</header>',
        source_header,
        content,
        flags=re.DOTALL
    )
    
    # Replace footer
    content = re.sub(
        r'<footer[^>]*class="[^"]*fl-builder-content[^"]*"[^>]*>.*?</footer>',
        source_footer,
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
print("Header/footer replaced, CSS/JS links untouched.")
