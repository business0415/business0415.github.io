#!/usr/bin/env python3
"""
Update URLs in careers/index.html to adjust for new path depth
"""

import os
import re
from pathlib import Path

def update_urls(file_path):
    """Update relative URLs to account for new directory depth"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Update relative paths that go up one level (../) to go up two levels (../../)
        # This is because we moved from /about/careers.html to /about/careers/index.html
        
        # Update href and src attributes
        # Pattern: href="../ or src="../
        content = re.sub(r'(href|src)="\.\.\/', r'\1="../../', content)
        
        # Update any remaining single ../ that might be in other contexts
        content = re.sub(r'url\(\.\.\/', r'url(../../', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

file_path = 'PumaPulse.rocks/about/careers/index.html'

print("🔧 UPDATING CAREERS PAGE URLS...\n")

if Path(file_path).exists():
    if update_urls(file_path):
        print(f"✓ Updated: {file_path}")
        print("\nAll relative URLs adjusted for new path depth.")
    else:
        print("No changes needed or file already updated.")
else:
    print(f"❌ File not found: {file_path}")

print("\n✅ DONE!")
