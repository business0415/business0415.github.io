#!/usr/bin/env python3
"""
Download Cloudinary images and replace URLs with local paths
"""

import os
import re
import urllib.request
import ssl
from pathlib import Path
from urllib.parse import urlparse

def download_image(url, save_path):
    """Download an image from URL"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Create SSL context that doesn't verify certificates
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Download the image
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=30, context=ssl_context) as response:
            with open(save_path, 'wb') as out_file:
                out_file.write(response.read())
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False

def extract_cloudinary_urls(file_path):
    """Extract all unique Cloudinary image URLs from HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all Cloudinary URLs
        pattern = r'https://res\.cloudinary\.com/di1g2wt1b/image/upload/[^"\'\s>]+'
        urls = set(re.findall(pattern, content))
        
        return urls
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return set()

def replace_cloudinary_urls(file_path, url_mapping):
    """Replace Cloudinary URLs with local paths"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for cloudinary_url, local_path in url_mapping.items():
            content = content.replace(cloudinary_url, local_path)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

# Files to process
html_files = [
    'PumaPulse.rocks/case-studies/index.html',
    'PumaPulse.rocks/resources/index.html',
]

print("📥 DOWNLOADING CLOUDINARY IMAGES...\n")
print("This will:")
print("  1. Extract all Cloudinary image URLs")
print("  2. Download images to local folder")
print("  3. Replace URLs with local paths\n")

# Create images directory
images_dir = 'PumaPulse.rocks/images'
os.makedirs(images_dir, exist_ok=True)

# Collect all unique URLs
all_urls = set()
for html_file in html_files:
    if Path(html_file).exists():
        urls = extract_cloudinary_urls(html_file)
        all_urls.update(urls)
        print(f"Found {len(urls)} images in {html_file}")

print(f"\nTotal unique images: {len(all_urls)}\n")

# Download images and create mapping
url_mapping = {}
downloaded = 0
failed = 0

for url in sorted(all_urls):
    # Extract filename from URL
    filename = url.split('/')[-1].split('?')[0]
    local_path = f'images/{filename}'
    save_path = f'{images_dir}/{filename}'
    
    print(f"Downloading: {filename}...")
    if download_image(url, save_path):
        url_mapping[url] = local_path
        downloaded += 1
    else:
        failed += 1

print(f"\n✅ Downloaded: {downloaded}")
print(f"❌ Failed: {failed}\n")

# Update HTML files
if url_mapping:
    print("Updating HTML files...")
    for html_file in html_files:
        if Path(html_file).exists():
            if replace_cloudinary_urls(html_file, url_mapping):
                print(f"✓ Updated: {html_file}")

print(f"\n🎉 DONE! Images are now hosted locally.")
print("This should fix the disappearing image issue!")
