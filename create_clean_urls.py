#!/usr/bin/env python3
import os
import re
from pathlib import Path
import shutil

def create_clean_urls():
    print("Creating clean URL structure...")
    
    # Get all HTML files except index.html
    html_files = [f for f in Path('.').glob('*.html') if f.name != 'index.html']
    
    for html_file in html_files:
        # Get the base name without extension
        base_name = html_file.stem
        
        # Create directory
        dir_path = Path(base_name)
        dir_path.mkdir(exist_ok=True)
        
        # Read the original file
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Only fix the essential paths for directory structure
        # Fix CSS paths
        content = re.sub(r'href="css/', 'href="../css/', content)
        # Fix JS paths  
        content = re.sub(r'src="js/', 'src="../js/', content)
        # Fix font paths in CSS
        content = re.sub(r"url\('fonts/", "url('../fonts/", content)
        content = re.sub(r'url\("fonts/', 'url("../fonts/', content)
        
        # Write to directory/index.html
        target_file = dir_path / 'index.html'
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Created: {base_name}/")
    
    # Remove original HTML files (except index.html)
    for html_file in html_files:
        html_file.unlink()
        print(f"✓ Removed: {html_file.name}")
    
    print(f"\nCompleted! Created {len(html_files)} clean URL directories.")

if __name__ == "__main__":
    create_clean_urls()