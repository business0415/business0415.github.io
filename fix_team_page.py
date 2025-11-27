#!/usr/bin/env python3
"""
Fix team page - disable SSCMBasePostFeed script
"""

import os
import re
from pathlib import Path

def disable_sscm_script(file_path):
    """Comment out SSCMBasePostFeed script"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Comment out the SSCMBasePostFeed script
        pattern = r'(<script[^>]*SSCMBasePostFeed[^>]*>.*?</script>)'
        content = re.sub(pattern, r'<!-- DISABLED: \1 -->', content, flags=re.DOTALL)
        
        # Also comment out the inline SSCMBasePostFeed configuration
        pattern2 = r'(window\.SpaceStation\.CommandModule\.SSCMBasePostFeed[^;]+;)'
        content = re.sub(pattern2, r'// DISABLED: \1', content)
        
        # Remove data attributes that trigger the script
        content = content.replace('data-sscmbasepostfeed', 'data-sscmbasepostfeed-disabled')
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# Fix team page
file_path = 'PumaPulse.rocks/about/team/index.html'

print("🔧 FIXING TEAM PAGE - DISABLING SSCMBasePostFeed...\n")

if Path(file_path).exists():
    if disable_sscm_script(file_path):
        print(f"✓ Fixed: {file_path}")
        print("\nTeam member photos will now stay visible!")
    else:
        print("Already fixed or no changes needed.")
else:
    print(f"❌ File not found: {file_path}")

print("\n✅ DONE!")
