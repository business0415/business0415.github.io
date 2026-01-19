# PumaPulse Website

This website is configured for GitHub Pages with clean URLs using Jekyll.

## Clean URLs Setup

The site uses Jekyll's `permalink: pretty` configuration to automatically create clean URLs:

- `pumapulse.org/` (instead of `pumapulse.org/index.html`)
- `pumapulse.org/about/` (instead of `pumapulse.org/aboutus.html`)
- `pumapulse.org/blog/` (instead of `pumapulse.org/blog.html`)
- And so on for all pages...

## How it works

1. **Jekyll Configuration**: The `_config.yml` file contains `permalink: pretty` which automatically handles URL rewriting
2. **Updated Links**: All internal links have been updated to use clean URLs (e.g., `href="/about/"` instead of `href="aboutus.html"`)
3. **GitHub Pages**: When deployed to GitHub Pages, Jekyll will automatically serve clean URLs

## Deployment

Simply push to your GitHub repository with GitHub Pages enabled. Jekyll will automatically:
- Process all HTML files
- Create clean URLs
- Generate a sitemap
- Serve your site with clean URLs

No additional configuration needed!