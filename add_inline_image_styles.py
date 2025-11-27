#!/usr/bin/env python3
"""
Add inline styles to all images to force them to stay visible
"""

import os
import re
from pathlib import Path

def add_inline_styles_to_images(file_path):
    """Add inline styles to all img tags"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changed = False
        
        # Pattern to find img tags
        # Add inline style to force visibility
        def add_style(match):
            img_tag = match.group(0)
            # Check if already has our protection style
            if 'opacity: 1 !important' in img_tag:
                return img_tag
            
            # Check if has style attribute
            if 'style=' in img_tag:
                # Add to existing style
                img_tag = re.sub(
                    r'style="([^"]*)"',
                    r'style="\1; opacity: 1 !important; visibility: visible !important; display: inline !important;"',
                    img_tag
                )
            else:
                # Add new style attribute before the closing >
                img_tag = img_tag.replace(
                    '>',
                    ' style="opacity: 1 !important; visibility: visible !important; display: inline !important;">',
                    1
                )
            return img_tag
        
        # Find all img tags and add inline styles
        pattern = r'<img[^>]*>'
        new_content = re.sub(pattern, add_style, content)
        
        if new_content != content:
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
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
    
    # Target specific problematic pages first
    priority_files = [
        'PumaPulse.rocks/case-studies/index.html',
        'PumaPulse.rocks/resources/index.html',
    ]
    
    print("Adding inline styles to force images visible...")
    print("Starting with priority pages:\n")
    
    fixed_count = 0
    for file_path in priority_files:
        if Path(file_path).exists():
            if add_inline_styles_to_images(file_path):
                print(f"✓ Fixed: {file_path}")
                fixed_count += 1
    
    # Now do all other HTML files
    print("\nProcessing all other HTML files...\n")
    
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html') and not file.endswith('.bak'):
                full_path = Path(root) / file
                if str(full_path) not in priority_files:
                    html_files.append(full_path)
    
    for html_file in html_files:
        if add_inline_styles_to_images(html_file):
            fixed_count += 1
    
    print(f"\n{'='*80}")
    print(f"Summary: Added inline styles to images in {fixed_count} HTML files")
    print(f"{'='*80}")
    print("\nAll images now have inline styles:")
    print("  opacity: 1 !important")
    print("  visibility: visible !important")
    print("  display: inline !important")
    print("\nThese inline styles have highest priority and cannot be overridden!")

if __name__ == '__main__':
    main()
