#!/usr/bin/env python3
"""
Add JavaScript to protect images from being hidden
"""

import os
from pathlib import Path

# JavaScript code to prevent images from being hidden
PROTECTION_SCRIPT = """
<script>
// Protect images from being hidden by other scripts
(function() {
    'use strict';
    
    // Prevent Nelio AB Testing from hiding content
    window.nabIsLoading = false;
    
    // Force all images to be visible
    function forceImagesVisible() {
        const images = document.querySelectorAll('img');
        images.forEach(img => {
            img.style.opacity = '1';
            img.style.visibility = 'visible';
            img.style.display = '';
            img.removeAttribute('hidden');
        });
    }
    
    // Run immediately
    forceImagesVisible();
    
    // Run after DOM is loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', forceImagesVisible);
    }
    
    // Run after everything is loaded
    window.addEventListener('load', forceImagesVisible);
    
    // Keep checking and fixing every 500ms for the first 5 seconds
    let checkCount = 0;
    const checkInterval = setInterval(() => {
        forceImagesVisible();
        checkCount++;
        if (checkCount >= 10) {
            clearInterval(checkInterval);
        }
    }, 500);
    
    // Observe DOM changes and fix images if they get hidden
    const observer = new MutationObserver(() => {
        forceImagesVisible();
    });
    
    // Start observing after DOM is ready
    if (document.body) {
        observer.observe(document.body, {
            attributes: true,
            attributeFilter: ['style', 'class', 'hidden'],
            subtree: true
        });
    } else {
        document.addEventListener('DOMContentLoaded', () => {
            observer.observe(document.body, {
                attributes: true,
                attributeFilter: ['style', 'class', 'hidden'],
                subtree: true
            });
        });
    }
})();
</script>
"""

def add_protection_script(file_path):
    """Add image protection script to HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if protection script is already added
        if 'Protect images from being hidden' in content:
            return False
        
        # Add script before closing </head> tag
        if '</head>' in content:
            content = content.replace('</head>', f'{PROTECTION_SCRIPT}\n</head>')
            
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
    
    print(f"Found {len(html_files)} HTML files...")
    print(f"Adding image protection JavaScript...\n")
    
    fixed_count = 0
    for html_file in html_files:
        if add_protection_script(html_file):
            print(f"✓ Protected: {html_file}")
            fixed_count += 1
    
    print(f"\n{'='*80}")
    print(f"Summary: Added protection to {fixed_count} out of {len(html_files)} HTML files")
    print(f"{'='*80}")
    print("\nImage protection script added!")
    print("This will:")
    print("  - Force all images to stay visible")
    print("  - Prevent scripts from hiding images")
    print("  - Monitor and fix images if they get hidden")
    print("  - Keep checking for 5 seconds after page load")

if __name__ == '__main__':
    main()
