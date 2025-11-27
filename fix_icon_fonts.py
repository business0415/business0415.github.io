#!/usr/bin/env python3
"""
Fix broken icon font paths across all HTML files
"""

import os
import re
from pathlib import Path

def fix_icon_paths(file_path):
    """Fix icon font paths to use CDN or correct relative paths"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix Font Awesome paths - use CDN instead
        # Replace local font-awesome with CDN
        fa_cdn = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" integrity="sha512-1ycn6IcaQQ40/MKBW2W4Rhis/DbILU74C1vSrLJxCq57o941Ym01SwNsOMqvEBFlcgUa6xLiPY/NS5R+E6ztJQ==" crossorigin="anonymous" referrerpolicy="no-referrer" />'
        
        # Remove broken local font-awesome links
        content = re.sub(r'<link[^>]*font-awesome[^>]*>', '', content)
        content = re.sub(r'<link[^>]*fontawesome[^>]*>', '', content)
        
        # Add CDN link before </head> if not already present
        if 'font-awesome' not in content and 'fontawesome' not in content:
            content = content.replace('</head>', f'{fa_cdn}\n</head>')
        
        # Fix ss-icons paths (space station icons)
        content = re.sub(
            r"href='wp-content/plugins/space-station-command-module/",
            r"href='../wp-content/plugins/space-station-command-module/",
            content
        )
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

# Find all HTML files
html_files = []
for root, dirs, files in os.walk('PumaPulse.rocks'):
    for file in files:
        if file.endswith('.html') and not file.endswith('.bak'):
            html_files.append(os.path.join(root, file))

print(f"🔧 FIXING ICON FONTS IN {len(html_files)} FILES...\n")

fixed_count = 0
for html_file in html_files:
    if fix_icon_paths(html_file):
        fixed_count += 1
        if fixed_count <= 10:  # Show first 10
            print(f"✓ Fixed: {html_file}")

if fixed_count > 10:
    print(f"... and {fixed_count - 10} more files")

print(f"\n✅ FIXED {fixed_count} FILES!")
print("Icon fonts now use CDN for Font Awesome.")
