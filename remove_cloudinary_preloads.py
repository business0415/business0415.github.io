#!/usr/bin/env python3
"""
Remove excessive Cloudinary preload tags that trigger rate limiting
"""

import os
import re
from pathlib import Path

def remove_cloudinary_preloads(file_path):
    """Remove Cloudinary image preload tags"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove all Cloudinary image preload tags (but keep logo)
        # Pattern: <link rel='preload' href='https://res.cloudinary.com/...jpg' as='image' .../>
        pattern = r"<link rel='preload' href='https://res\.cloudinary\.com/[^']+\.(?:jpg|png|webp|jpeg)'[^>]*/?>"
        
        # Count matches
        matches = re.findall(pattern, content)
        
        # Keep only the logo preload, remove all image preloads
        for match in matches:
            if 'logo.svg' not in match:  # Keep logo
                content = content.replace(match, '')
        
        # Clean up extra blank lines
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return len(matches) - 1  # -1 for logo
        
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 0

# Fix the problematic pages
priority_files = [
    'PumaPulse.rocks/case-studies/index.html',
    'PumaPulse.rocks/resources/index.html',
]

print("🔧 REMOVING EXCESSIVE CLOUDINARY PRELOADS...\n")
print("This will fix the rate limiting issue by:")
print("  - Removing image preload tags")
print("  - Keeping only the logo preload")
print("  - Letting images load naturally\n")

total_removed = 0
for file_path in priority_files:
    if Path(file_path).exists():
        removed = remove_cloudinary_preloads(file_path)
        if removed > 0:
            print(f"✓ {file_path}")
            print(f"  Removed {removed} preload tags")
            total_removed += removed

print(f"\n✅ FIXED! Removed {total_removed} excessive preload tags")
print("\nThis should solve the rate limiting issue!")
print("Images will now load naturally without overwhelming Cloudinary.")
