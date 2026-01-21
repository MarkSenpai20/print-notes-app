# Vantal Links

A personalized link aggregator web application that embeds multiple websites in a single dashboard.

## Features

- 🎨 Clean, modern interface with MJ branding
- 📋 Table of contents for easy navigation
- 🔗 Embed both hosted websites and local HTML files
- ⚡ One-click redirection to any link
- 📊 Dashboard with usage statistics
- 🔧 Easy configuration via Python CLI

## File Structure

- `index.html` - Main web application
- `config.json` - Configuration file with all links
- `config.py` - Python CLI for managing links
- `README.md` - This documentation file

## Setup Instructions

### Option 1: GitHub Pages (Recommended)

1. Upload all files to a GitHub repository
2. Enable GitHub Pages in repository settings
3. Access your Vantal Links at `https://<username>.github.io/<repository>`

### Option 2: Local Development

1. Clone/download the files to your computer
2. Open `index.html` in a web browser
3. Use the Python CLI to manage links

## Managing Links

### Using the Python CLI

1. Make sure you have Python 3 installed
2. Run the configuration wizard:
   ```bash
   python config.py