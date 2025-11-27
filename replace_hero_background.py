#!/usr/bin/env python3
"""
Replace Spline 3D viewer with background image
"""

import re
from pathlib import Path

file_path = 'PumaPulse.rocks/index.html'

print("🔧 REPLACING HERO BACKGROUND...\n")

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# Find the row with Spline viewer and change it to use background image
# Change fl-row-bg-embed to fl-row-bg-photo
content = re.sub(
    r'(<div class="fl-row fl-row-full-width )fl-row-bg-embed( fl-node-93euck8p15qw[^>]*>)',
    r'\1fl-row-bg-photo\2',
    content
)

# Remove the Spline embed code
content = re.sub(
    r'<div class="fl-bg-embed-code">\s*<spline-viewer[^>]*></spline-viewer>\s*</div>',
    '',
    content
)

# Add background image styling to the row
# Find the row node and add inline style
content = re.sub(
    r'(data-node="93euck8p15qw">)',
    r'\1\n\t<div class="fl-row-bg-photo" style="background-image: url(\'wp-content/uploads/hero-background.webp\'); background-size: cover; background-position: center; background-repeat: no-repeat;"></div>',
    content
)

if content != original:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Updated: {file_path}")
    print("\nChanges made:")
    print("  - Removed Spline 3D viewer")
    print("  - Added hero-background.webp as background")
    print("  - Set to cover and center")
else:
    print("  No changes made")

print("\n✅ DONE!")
