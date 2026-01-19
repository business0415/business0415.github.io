#!/usr/bin/env python3
import os
import re
from pathlib import Path

def remove_tawk():
    print("Removing Tawk.to from all files...")
    
    # Process main index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = re.sub(r'<!--Start of Tawk\.to Script-->.*?<!--End of Tawk\.to Script-->', '', content, flags=re.DOTALL)
    content = re.sub(r'<script[^>]*>.*?Tawk.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'.*Tawk.*\r?\n', '', content)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Cleaned: index.html")
    
    # Process all directory files
    exclude_dirs = {'css', 'js', 'fonts', 'category', '.git', '.vscode'}
    directories = [d for d in Path('.').iterdir() if d.is_dir() and d.name not in exclude_dirs]
    
    for dir_path in directories:
        index_file = dir_path / 'index.html'
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            content = re.sub(r'<!--Start of Tawk\.to Script-->.*?<!--End of Tawk\.to Script-->', '', content, flags=re.DOTALL)
            content = re.sub(r'<script[^>]*>.*?Tawk.*?</script>', '', content, flags=re.DOTALL)
            content = re.sub(r'.*Tawk.*\r?\n', '', content)
            
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Cleaned: {dir_path.name}/")
    
    # Process category files
    category_files = list(Path('category').glob('*.html'))
    for file_path in category_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = re.sub(r'<!--Start of Tawk\.to Script-->.*?<!--End of Tawk\.to Script-->', '', content, flags=re.DOTALL)
        content = re.sub(r'<script[^>]*>.*?Tawk.*?</script>', '', content, flags=re.DOTALL)
        content = re.sub(r'.*Tawk.*\r?\n', '', content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Cleaned: category/{file_path.name}")
    
    print("Completed! Tawk.to removed from all files.")

if __name__ == "__main__":
    remove_tawk()