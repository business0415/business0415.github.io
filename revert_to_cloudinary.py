#!/usr/bin/env python3
"""
Revert back to Cloudinary URLs
"""

import os
import re
from pathlib import Path

def revert_to_cloudinary(file_path):
    """Revert local image paths back to Cloudinary URLs"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Map local paths back to Cloudinary URLs
        replacements = {
            'images/01-Featured-Image-Thumbnail-300x212.jpg': 'https://res.cloudinary.com/di1g2wt1b/image/upload/PumaPulse-2025.b-cdn.net/wp-content/uploads/2025/09/01-Featured-Image-Thumbnail-300x212.jpg',
            'images/01-Refresh-vs-Redesign-Graphic-300x150.jpg': 'https://res.cloudinary.com/di1g2wt1b/image/upload/PumaPulse-2025.b-cdn.net/wp-content/uploads/2025/08/01-Refresh-vs-Redesign-Graphic-300x150.jpg',
            'images/01-Schoox-Featured-Image-300x212.jpg': 'https://res.cloudinary.com/di1g2wt1b/image/upload/PumaPulse-2025.b-cdn.net/wp-content/uploads/2025/10/01-Schoox-Featured-Image-300x212.jpg',
            'images/abc-fitness-thumbnail-300x212.jpg': 'https://res.cloudinary.com/di1g2wt1b/image/upload/PumaPulse-2025.b-cdn.net/wp-content/uploads/2025/08/abc-fitness-thumbnail-300x212.jpg',
            'images/aerotech-featured-300x212.jpg': 'https://res.cloudinary.com/di1g2wt1b/image/upload/PumaPulse-2025.b-cdn.net/wp-content/uploads/2025/08/aerotech-featured-300x212.jpg',
            'images/bizrate-featured-300x212.jpg': 'https://res.cloudinary.com/di1g2wt1b/image/upload/PumaPulse-2025.b-cdn.net/wp-content/uploads/2025/08/bizrate-featured-300x212.jpg',
            'images/boston-dynamics-featured-300x212.jpg': 'https://res.cloudinary.com/di1g2wt1b/image/upload/PumaPulse-2025.b-cdn.net/wp-content/uploads/2025/08/boston-dynamics-featured-300x212.jpg',
            'images/Choose-Agency-Featured-300x150.jpg': 'https://res.cloudinary.com/di1g2wt1b/image/upload/PumaPulse-2025.b-cdn.net/wp-content/uploads/2022/10/Choose-Agency-Featured-300x150.jpg',
            'images/Creative-1-300x150.jpg': 'https://res.cloudinary.com/di1g2wt1b/image/upload/PumaPulse-2025.b-cdn.net/wp-content/uploads/2025/09/Creative-1-300x150.jpg',
            'images/cropped-PumaPulse-symbol-round-180x180.png': 'https://res.cloudinary.com/di1g2wt1b/image/upload/PumaPulse-2025.b-cdn.net/wp-content/uploads/2025/09/cropped-PumaPulse-symbol-round-180x180.png',
            'images/Featured-Image-300x150.jpg': 'https://res.cloudinary.com/di1g2wt1b/image/upload/PumaPulse-2025.b-cdn.net/wp-content/uploads/2025/10/Featured-Image-300x150.jpg',
            'images/Featured-Image-Free-University-Courses-300x150.jpg': 'https://res.cloudinary.com/di1g2wt1b/image/upload/PumaPulse-2025.b-cdn.net/wp-content/uploads/2024/06/Featured-Image-Free-University-Courses-300x150.jpg',
            'images/hitt-thumbnail-300x212.jpg': 'https://res.cloudinary.com/di1g2wt1b/image/upload/PumaPulse-2025.b-cdn.net/wp-content/uploads/2025/08/hitt-thumbnail-300x212.jpg',
            'images/hysafe-thumbnail-300x212.jpg': 'https://res.cloudinary.com/di1g2wt1b/image/upload/PumaPulse-2025.b-cdn.net/wp-content/uploads/2025/08/hysafe-thumbnail-300x212.jpg',
            'images/logo2.png': 'https://res.cloudinary.com/di1g2wt1b/image/upload/PumaPulse-2025.b-cdn.net/wp-content/uploads/2025/06/logo2.png',
            'images/marketing-archetype-quiz-resized-300x150.jpg': 'https://res.cloudinary.com/di1g2wt1b/image/upload/PumaPulse-2025.b-cdn.net/wp-content/uploads/2025/08/marketing-archetype-quiz-resized-300x150.jpg',
            'images/mdisrupt-thumbnail-300x212.jpg': 'https://res.cloudinary.com/di1g2wt1b/image/upload/PumaPulse-2025.b-cdn.net/wp-content/uploads/2025/08/mdisrupt-thumbnail-300x212.jpg',
            'images/skyline-construction-thumbnail-300x212.jpg': 'https://res.cloudinary.com/di1g2wt1b/image/upload/PumaPulse-2025.b-cdn.net/wp-content/uploads/2025/08/skyline-construction-thumbnail-300x212.jpg',
            'images/Web-Design-Process-Featured-300x150.jpg': 'https://res.cloudinary.com/di1g2wt1b/image/upload/PumaPulse-2025.b-cdn.net/wp-content/uploads/2025/07/Web-Design-Process-Featured-300x150.jpg',
            'images/website-cost-calculator-thumbnail-300x150.jpg': 'https://res.cloudinary.com/di1g2wt1b/image/upload/PumaPulse-2025.b-cdn.net/wp-content/uploads/2025/06/website-cost-calculator-thumbnail-300x150.jpg',
            'images/website-improvement-plan-thumbnail-300x150.jpg': 'https://res.cloudinary.com/di1g2wt1b/image/upload/PumaPulse-2025.b-cdn.net/wp-content/uploads/2025/08/website-improvement-plan-thumbnail-300x150.jpg',
            'images/website-redesign-project-plan-thumbnail-300x150.jpg': 'https://res.cloudinary.com/di1g2wt1b/image/upload/PumaPulse-2025.b-cdn.net/wp-content/uploads/2025/08/website-redesign-project-plan-thumbnail-300x150.jpg',
            'images/Website-Redesign-SEO-Value-Featured-300x150.jpg': 'https://res.cloudinary.com/di1g2wt1b/image/upload/PumaPulse-2025.b-cdn.net/wp-content/uploads/2023/03/Website-Redesign-SEO-Value-Featured-300x150.jpg',
        }
        
        for local_path, cloudinary_url in replacements.items():
            content = content.replace(local_path, cloudinary_url)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# Files to revert
html_files = [
    'PumaPulse.rocks/case-studies/index.html',
    'PumaPulse.rocks/resources/index.html',
]

print("🔄 REVERTING TO CLOUDINARY URLS...\n")

for html_file in html_files:
    if Path(html_file).exists():
        if revert_to_cloudinary(html_file):
            print(f"✓ Reverted: {html_file}")

print("\n✅ REVERTED! Back to using Cloudinary URLs")
