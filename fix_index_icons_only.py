#!/usr/bin/env python3
"""
Fix only icon fonts in index.html without changing structure
"""

import os
import re
from pathlib import Path

def fix_icons_only(file_path):
    """Fix icon fonts only"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Add Font Awesome CDN if not present
        fa_cdn = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" integrity="sha512-1ycn6IcaQQ40/MKBW2W4Rhis/DbILU74C1vSrLJxCq57o941Ym01SwNsOMqvEBFlcgUa6xLiPY/NS5R+E6ztJQ==" crossorigin="anonymous" referrerpolicy="no-referrer" />'
        
        # Check if Font Awesome CDN is already present
        if 'cdnjs.cloudflare.com/ajax/libs/font-awesome' not in content:
            # Add before </head>
            content = content.replace('</head>', f'{fa_cdn}\n</head>')
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

file_path = 'PumaPulse.rocks/index.html'

print("🔧 FIXING ICONS IN INDEX.HTML...\n")

if Path(file_path).exists():
    if fix_icons_only(file_path):
        print(f"✓ Fixed: {file_path}")
        print("\nIcons fixed, structure unchanged.")
    else:
        print("Already has Font Awesome CDN or no changes needed.")
else:
    print(f"❌ File not found: {file_path}")

print("\n✅ DONE!")
