#!/usr/bin/env python3
"""
Disable Nelio AB Testing that might be causing image issues
"""

import os
import re
from pathlib import Path

def disable_nelio_testing(file_path):
    """Remove or disable Nelio AB Testing scripts"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changed = False
        
        # Remove the Nelio AB Testing overlay style that might hide content
        if 'nelio-ab-testing-overlay' in content:
            # Comment out the problematic overlay style
            pattern = r'(<style id="nelio-ab-testing-overlay"[^>]*>.*?</style>)'
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, r'<!-- Nelio AB Testing Disabled \1 -->', content, flags=re.DOTALL)
                changed = True
        
        # Remove or disable the Nelio AB Testing JavaScript
        if 'nelio-ab-testing-main-js' in content:
            pattern = r'(<script[^>]*id="nelio-ab-testing-main-js[^>]*>.*?</script>)'
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, r'<!-- Nelio AB Testing JS Disabled \1 -->', content, flags=re.DOTALL)
                changed = True
        
        # Set nabIsLoading to false to prevent hiding
        if 'window.nabIsLoading=true' in content:
            content = content.replace('window.nabIsLoading=true', 'window.nabIsLoading=false')
            changed = True
        
        if changed:
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function"""
    base_dir = Path('PumaPulse.rocks')
    
    if not base_dir.exists():
        print(f"Error: {base_dir} directory not found!")
        return
    
    # Find all HTML files (excluding .bak files)
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html') and not file.endswith('.bak'):
                html_files.append(Path(root) / file)
    
    print(f"Found {len(html_files)} HTML files to check...")
    print(f"Disabling Nelio AB Testing that might be hiding images...\n")
    
    fixed_count = 0
    for html_file in html_files:
        if disable_nelio_testing(html_file):
            print(f"✓ Fixed: {html_file}")
            fixed_count += 1
    
    print(f"\n{'='*80}")
    print(f"Summary: Fixed {fixed_count} out of {len(html_files)} HTML files")
    print(f"{'='*80}")
    print("\nNelio AB Testing has been disabled.")
    print("This should prevent the overlay from hiding your images!")

if __name__ == '__main__':
    main()
