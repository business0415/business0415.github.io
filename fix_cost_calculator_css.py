#!/usr/bin/env python3
"""
Fix CSS bundle reference for website-cost-calculator
"""

import re
from pathlib import Path

file_path = 'PumaPulse.rocks/resources/website-cost-calculator/index.html'

# Correct bundle hash from working page
correct_bundle = '9bab89614da209c2788314d4fdf4f0e0'

print("🔧 FIXING CSS BUNDLE FOR COST CALCULATOR...\n")

if not Path(file_path).exists():
    print(f"❌ Not found: {file_path}")
    exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# Replace the old bundle hash with the correct one
content = re.sub(
    r'fl-builder-layout-bundle-[a-f0-9]+-css',
    f'fl-builder-layout-bundle-{correct_bundle}-css',
    content
)

content = re.sub(
    r'cache/[a-f0-9]+-layout-bundled635\.css',
    f'cache/{correct_bundle}-layout-bundled635.css',
    content
)

if content != original:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Fixed: {file_path}")
else:
    print(f"  No changes: {file_path}")

print("\n✅ DONE!")
print("CSS bundle updated.")
