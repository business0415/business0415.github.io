#!/usr/bin/env python3
"""
Disable SSCMBasePostFeed JavaScript that's hiding images
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

# Files to fix
html_files = [
    'PumaPulse.rocks/case-studies/index.html',
    'PumaPulse.rocks/resources/index.html',
]

print("🔧 DISABLING SSCMBasePostFeed SCRIPT...\n")
print("This script manages the post feed and may be hiding images.\n")

for html_file in html_files:
    if Path(html_file).exists():
        if disable_sscm_script(html_file):
            print(f"✓ Disabled: {html_file}")

print("\n✅ SSCMBasePostFeed DISABLED!")
print("Images should now stay visible in the UL list.")
