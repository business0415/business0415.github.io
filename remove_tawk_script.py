#!/usr/bin/env python3
"""
Script to remove specific Tawk.to script lines from HTML files
"""

import os
import re
import json
from pathlib import Path

def remove_tawk_script(file_path):
    """
    Remove the specific Tawk.to script line from an HTML file
    Returns True if changes were made, False otherwise
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        original_content = content
        
        # Pattern to match the specific Tawk.to script line
        pattern = r"s1\.src = 'https://embed\.tawk\.to/676134feaf5bfec1dbdd5a5b/1if9re0vu';"
        
        # Remove the line
        content = re.sub(pattern, '', content)
        
        # Check if any changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def find_and_process_html_files(root_dir='.'):
    """
    Find all HTML files and process them to remove Tawk.to scripts
    """
    results = {
        'processed_files': [],
        'modified_files': [],
        'errors': [],
        'total_files': 0,
        'total_modified': 0
    }
    
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    results['total_files'] = len(html_files)
    
    print(f"Found {len(html_files)} HTML files to process...")
    
    for file_path in html_files:
        try:
            results['processed_files'].append(file_path)
            
            if remove_tawk_script(file_path):
                results['modified_files'].append(file_path)
                results['total_modified'] += 1
                print(f"✓ Modified: {file_path}")
            else:
                print(f"- No changes: {file_path}")
                
        except Exception as e:
            error_msg = f"Error processing {file_path}: {e}"
            results['errors'].append(error_msg)
            print(f"✗ {error_msg}")
    
    return results

def main():
    """
    Main function to execute the script
    """
    print("Starting Tawk.to script removal process...")
    print("=" * 50)
    
    # Process all HTML files
    results = find_and_process_html_files()
    
    # Print summary
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print(f"Total HTML files found: {results['total_files']}")
    print(f"Files modified: {results['total_modified']}")
    print(f"Errors encountered: {len(results['errors'])}")
    
    if results['errors']:
        print("\nErrors:")
        for error in results['errors']:
            print(f"  - {error}")
    
    # Save detailed results to JSON file
    with open('tawk_removal_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nDetailed results saved to: tawk_removal_results.json")
    
    if results['total_modified'] > 0:
        print(f"\n✓ Successfully removed Tawk.to scripts from {results['total_modified']} files!")
    else:
        print("\n- No files needed modification.")

if __name__ == "__main__":
    main()