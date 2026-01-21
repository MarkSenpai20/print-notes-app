#!/usr/bin/env python3
"""
Vantal Links Configuration Wizard
This script helps manage the config.json file for the Vantal Links web app.
Run with: python config.py
"""

import json
import os
import sys
import subprocess
from datetime import datetime

CONFIG_FILE = "config.json"

def load_config():
    """Load existing configuration from config.json"""
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"⚠️  {CONFIG_FILE} not found. Creating new configuration...")
        return {"links": []}
    except json.JSONDecodeError:
        print(f"❌ Error: {CONFIG_FILE} contains invalid JSON.")
        sys.exit(1)

def save_config(config):
    """Save configuration to config.json"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"✅ Configuration saved to {CONFIG_FILE}")

def display_current_links(config):
    """Display current links in the configuration"""
    if not config.get("links"):
        print("📭 No links currently configured.")
        return
    
    print("\n" + "="*60)
    print("📋 CURRENT LINKS")
    print("="*60)
    for i, link in enumerate(config["links"], 1):
        print(f"{i:2}. {link['name']}")
        print(f"    URL: {link['url']}")
        print(f"    Icon: {link.get('icon', 'fas fa-link')}")
        print()

def add_new_link(config):
    """Add a new link to the configuration"""
    print("\n" + "="*60)
    print("➕ ADD NEW LINK")
    print("="*60)
    
    name = input("Enter link name: ").strip()
    if not name:
        print("❌ Link name cannot be empty.")
        return False
    
    url = input("Enter URL (http:// or https:// for web, filename for local): ").strip()
    if not url:
        print("❌ URL cannot be empty.")
        return False
    
    print("\n📊 Common Font Awesome icons:")
    print("  - Web: fab fa-chrome, fab fa-firefox")
    print("  - Social: fab fa-twitter, fab fa-linkedin, fab fa-facebook")
    print("  - Files: fas fa-file-code, fas fa-file-pdf")
    print("  - General: fas fa-link, fas fa-globe")
    print("  See all: https://fontawesome.com/icons")
    
    icon = input("Enter Font Awesome icon class (e.g., 'fas fa-globe'): ").strip()
    if not icon:
        icon = "fas fa-link"
    
    # Add the new link
    new_link = {
        "name": name,
        "url": url,
        "icon": icon
    }
    
    config["links"].append(new_link)
    print(f"✅ Added '{name}' to configuration.")
    return True

def remove_link(config):
    """Remove a link from the configuration"""
    if not config.get("links"):
        print("❌ No links to remove.")
        return False
    
    display_current_links(config)
    
    try:
        choice = int(input("\nEnter the number of the link to remove: "))
        if 1 <= choice <= len(config["links"]):
            removed = config["links"].pop(choice - 1)
            print(f"✅ Removed '{removed['name']}' from configuration.")
            return True
        else:
            print("❌ Invalid selection.")
            return False
    except ValueError:
        print("❌ Please enter a valid number.")
        return False

def edit_link(config):
    """Edit an existing link"""
    if not config.get("links"):
        print("❌ No links to edit.")
        return False
    
    display_current_links(config)
    
    try:
        choice = int(input("\nEnter the number of the link to edit: "))
        if 1 <= choice <= len(config["links"]):
            link = config["links"][choice - 1]
            print(f"\n📝 Editing '{link['name']}':")
            
            new_name = input(f"New name [{link['name']}]: ").strip()
            if new_name:
                link['name'] = new_name
            
            new_url = input(f"New URL [{link['url']}]: ").strip()
            if new_url:
                link['url'] = new_url
            
            new_icon = input(f"New icon [{link.get('icon', 'fas fa-link')}]: ").strip()
            if new_icon:
                link['icon'] = new_icon
            
            print(f"✅ Updated '{link['name']}'.")
            return True
        else:
            print("❌ Invalid selection.")
            return False
    except ValueError:
        print("❌ Please enter a valid number.")
        return False

def reorder_links(config):
    """Reorder links in the configuration"""
    if not config.get("links"):
        print("❌ No links to reorder.")
        return False
    
    display_current_links(config)
    
    try:
        print("\n🔄 REORDER LINKS")
        print("Enter the current numbers in the new order, separated by commas.")
        print(f"Example: 3,1,2,4,5 for {len(config['links'])} links")
        
        order_input = input("New order: ").strip()
        order_indices = [int(i.strip()) - 1 for i in order_input.split(',')]
        
        # Validate the input
        if set(order_indices) != set(range(len(config["links"]))):
            print("❌ Invalid order. Must include all links exactly once.")
            return False
        
        # Reorder the links
        config["links"] = [config["links"][i] for i in order_indices]
        print("✅ Links reordered successfully.")
        return True
    except (ValueError, IndexError):
        print("❌ Invalid input. Please enter valid numbers.")
        return False

def git_operations():
    """Perform Git operations to commit and push changes"""
    print("\n" + "="*60)
    print("🚀 GIT OPERATIONS")
    print("="*60)
    
    # Check if we're in a git repository
    try:
        subprocess.run(["git", "status"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Not a git repository or git not installed.")
        return False
    
    # Get commit message
    commit_msg = input("Enter commit message: ").strip()
    if not commit_msg:
        commit_msg = f"Update Vantal Links configuration - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    try:
        # Add changes
        print("🔄 Adding changes to git...")
        subprocess.run(["git", "add", CONFIG_FILE], check=True)
        
        # Commit changes
        print("💾 Committing changes...")
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        
        # Push changes
        print("🚀 Pushing to remote repository...")
        subprocess.run(["git", "push"], check=True)
        
        print("✅ Successfully committed and pushed changes!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        return False

def main_menu():
    """Display main menu and handle user choices"""
    config = load_config()
    
    while True:
        print("\n" + "="*60)
        print("🌟 VANTAL LINKS CONFIGURATION WIZARD")
        print("="*60)
        print(f"📊 Currently managing {len(config.get('links', []))} links")
        print()
        print("1. View current links")
        print("2. Add new link")
        print("3. Edit existing link")
        print("4. Remove link")
        print("5. Reorder links")
        print("6. Save configuration")
        print("7. Save and commit to Git")
        print("8. Exit")
        print("="*60)
        
        choice = input("\nSelect an option (1-8): ").strip()
        
        if choice == "1":
            display_current_links(config)
        elif choice == "2":
            if add_new_link(config):
                save_config(config)
        elif choice == "3":
            if edit_link(config):
                save_config(config)
        elif choice == "4":
            if remove_link(config):
                save_config(config)
        elif choice == "5":
            if reorder_links(config):
                save_config(config)
        elif choice == "6":
            save_config(config)
        elif choice == "7":
            save_config(config)
            if git_operations():
                print("\n✅ Configuration updated and committed successfully!")
                print("🌐 Your Vantal Links website will update after GitHub Pages rebuilds.")
        elif choice == "8":
            print("\n👋 Exiting. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1-8.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    print("🌟 Welcome to Vantal Links Configuration Wizard!")
    print("This tool helps you manage the links in your Vantal Links web app.")
    print()
    
    # Check for required files
    if not os.path.exists(CONFIG_FILE):
        print(f"⚠️  {CONFIG_FILE} not found. Creating new configuration...")
        with open(CONFIG_FILE, 'w') as f:
            json.dump({"links": []}, f, indent=2)
    
    main_menu()