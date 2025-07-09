#!/usr/bin/env python3
"""
Installation script for AIDA Agent App
"""

import frappe
from frappe.utils import get_site_url

def install_aida_agent():
    """
    Complete installation and setup of AIDA Agent App
    """
    print("Starting AIDA Agent installation...")
    
    try:
        # 1. Create AIDA Agent Settings document
        create_settings_document()
        
        # 2. Clear cache to ensure new assets are loaded
        frappe.clear_cache()
        
        # 3. Build assets
        build_assets()
        
        print("✅ AIDA Agent installation completed successfully!")
        print("\n📋 Next steps:")
        print("1. Restart your bench server: bench restart")
        print("2. Visit /aida_agent page to access AIDA Agent")
        print("3. Configure settings at /app/aida-agent-settings/AIDA%20Agent%20Settings")
        
    except Exception as e:
        print(f"❌ Installation failed: {str(e)}")
        frappe.log_error(f"AIDA Agent installation error: {str(e)}", "AIDA Installation")
        raise

def create_settings_document():
    """
    Create AIDA Agent Settings document with default values
    """
    try:
        # Check if settings already exist
        settings = frappe.get_single("AIDA Agent Settings")
        print("✅ AIDA Agent Settings already exist")
        return settings
    except frappe.DoesNotExistError:
        pass
    
    print("📝 Creating AIDA Agent Settings document...")
    
    # Create new settings document
    settings = frappe.new_doc("AIDA Agent Settings")
    
    # Set default values
    settings.update({
        "api_server_url": "http://localhost:5000",
        "erpnext_url": get_site_url(frappe.local.site),
        "google_api_key": "",
        "mongo_uri": "",
        "enable_onboarding": 1,
        "enable_lead_creation": 1,
        "widget_position": "bottom-right",
        "widget_theme": "light"
    })
    
    # Save the document
    settings.save()
    frappe.db.commit()
    
    print("✅ AIDA Agent Settings created successfully")
    print(f"   - API Server URL: {settings.api_server_url}")
    print(f"   - ERPNext URL: {settings.erpnext_url}")
    print(f"   - Widget Position: {settings.widget_position}")
    print(f"   - Widget Theme: {settings.widget_theme}")
    
    return settings

def build_assets():
    """
    Build and compile assets for the app
    """
    try:
        print("🔨 Building assets...")
        
        # Import build function
        from frappe.build import bundle
        
        # Build assets for the app
        bundle("aida_agent_app", verbose=True)
        
        print("✅ Assets built successfully")
        
    except Exception as e:
        print(f"⚠️  Asset building failed: {str(e)}")
        print("   This is not critical - assets may still work")

def check_installation():
    """
    Check if AIDA Agent is properly installed
    """
    print("🔍 Checking AIDA Agent installation...")
    
    # Check if app is installed
    installed_apps = frappe.get_installed_apps()
    if "aida_agent_app" not in installed_apps:
        print("❌ AIDA Agent App is not installed")
        return False
    
    print("✅ AIDA Agent App is installed")
    
    # Check if settings document exists
    try:
        settings = frappe.get_single("AIDA Agent Settings")
        print("✅ AIDA Agent Settings document exists")
    except:
        print("❌ AIDA Agent Settings document not found")
        return False
    
    # Check if assets exist
    import os
    css_path = frappe.get_app_path("aida_agent_app", "public", "css", "aida_agent.css")
    js_path = frappe.get_app_path("aida_agent_app", "public", "js", "aida_agent.js")
    
    if os.path.exists(css_path):
        print("✅ CSS assets found")
    else:
        print("❌ CSS assets not found")
        return False
        
    if os.path.exists(js_path):
        print("✅ JS assets found")
    else:
        print("❌ JS assets not found")
        return False
    
    print("✅ AIDA Agent installation is complete and healthy")
    return True

if __name__ == "__main__":
    install_aida_agent()