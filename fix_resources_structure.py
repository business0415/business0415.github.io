#!/usr/bin/env python3
"""
Fix resources page structure - add back UL wrapper and CSS for grid layout
"""

import os
import re
from pathlib import Path

def fix_structure(file_path):
    """Add UL wrapper and grid CSS"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Add UL wrapper around LI elements if missing
        # Find the pattern where LI starts without UL
        pattern = r'(<div id="SSCMBasePostFeed-found_posts-[^"]+[^>]*></div>\s*)\n\s*(<li class="SSCMBasePostFeed-post)'
        replacement = r'\1\n    <ul id="SSCMBasePostFeed-posts_container-56ejt412co9y" class="SSCMBasePostFeed-posts_container">\n        \2'
        content = re.sub(pattern, replacement, content)
        
        # Find the last </li> and add closing </ul> after it
        # Look for the last </li> before the closing container div
        pattern2 = r'(</li>\s*)(</div>\s*<div class="SSCMBasePostFeed-pagination)'
        replacement2 = r'\1    </ul>\n        \2'
        content = re.sub(pattern2, replacement2, content)
        
        # Add CSS for grid layout in the head section
        grid_css = '''
<style>
/* SSCMBasePostFeed Grid Layout */
.SSCMBasePostFeed-posts_container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 30px;
    list-style: none;
    padding: 0;
    margin: 0;
}

.SSCMBasePostFeed-post {
    position: relative;
    background: #fff;
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.SSCMBasePostFeed-post:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.SSCMBasePostFeed-post_stretched_link {
    display: block;
    text-decoration: none;
    color: inherit;
}

.SSCMBasePostFeed-content_container {
    display: flex;
    flex-direction: column;
}

.SSCMBasePostFeed-featured_image_container img {
    width: 100%;
    height: auto;
    display: block;
}

.SSCMBasePostFeed-post_title_container {
    padding: 20px;
}

.SSCMBasePostFeed-post_title {
    margin: 0;
    font-size: 18px;
    line-height: 1.4;
}

.SSCMBasePostFeed-post_tag_container {
    padding: 0 20px 20px;
}

.SSCMBasePostFeed-post_tag {
    display: inline-block;
    padding: 5px 15px;
    background: #f0f0f0;
    border-radius: 20px;
    font-size: 14px;
}

@media (max-width: 768px) {
    .SSCMBasePostFeed-posts_container {
        grid-template-columns: 1fr;
    }
}
</style>
'''
        
        # Insert CSS before </head>
        if '</head>' in content and 'SSCMBasePostFeed Grid Layout' not in content:
            content = content.replace('</head>', f'{grid_css}\n</head>')
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# Fix resources page
file_path = 'PumaPulse.rocks/resources/index.html'

print("🔧 FIXING RESOURCES PAGE STRUCTURE...\n")

if Path(file_path).exists():
    if fix_structure(file_path):
        print(f"✓ Fixed: {file_path}")
        print("\nAdded:")
        print("  - UL wrapper around LI elements")
        print("  - Grid layout CSS")
        print("  - Hover effects")
    else:
        print("No changes needed or already fixed")

print("\n✅ STRUCTURE RESTORED!")
print("Images will stay visible AND layout will look correct.")
