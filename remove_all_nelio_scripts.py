#!/usr/bin/env python3
"""
Remove ALL Nelio AB Testing scripts completely
"""

import os
import re
from pathlib import Path

def remove_nelio_scripts(file_path):
    """Remove all Nelio AB Testing scripts"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove ALL Nelio script tags (even the visitor-type one)
        patterns = [
            r'<script[^>]*nelio-ab-testing[^>]*>.*?</script>',
            r'<script[^>]*nelio-ab-testing[^>]*/>',
            r'<script[^>]*nelio-ab-testing[^>]*></script>',
        ]
        
        for pattern in patterns:
            content = re.sub(pattern, '<!-- Nelio AB Testing Script Removed -->', content, flags=re.DOTALL)
        
        # Also remove any Nelio window variables
        nelio_vars = [
            r'window\.nabIsLoading\s*=\s*[^;]+;',
            r'window\.nabSettings\s*=\s*[^;]+;',
        ]
        
        for pattern in nelio_vars:
            content = re.sub(pattern, '', content)
        
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

print("🗑️ REMOVING ALL NELIO AB TESTING SCRIPTS...\n")

for html_file in html_files:
    if Path(html_file).exists():
        if remove_nelio_scripts(html_file):
            print(f"✓ Cleaned: {html_file}")

print("\n✅ ALL NELIO SCRIPTS REMOVED!")
print("This should stop any AB testing interference with images.")
