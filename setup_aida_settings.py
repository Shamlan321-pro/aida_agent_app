#!/usr/bin/env python3
"""
Script to initialize AIDA Agent Settings
"""

import frappe
from frappe.utils import get_site_url

def setup_aida_settings():
    """
    Create and configure AIDA Agent Settings document
    """
    try:
        # Check if settings already exist
        try:
            settings = frappe.get_single("AIDA Agent Settings")
            print("AIDA Agent Settings already exist")
            return settings
        except frappe.DoesNotExistError:
            pass
        
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
        
        print("AIDA Agent Settings created successfully!")
        print(f"Settings configured with:")
        print(f"  - API Server URL: {settings.api_server_url}")
        print(f"  - ERPNext URL: {settings.erpnext_url}")
        print(f"  - Widget Position: {settings.widget_position}")
        print(f"  - Widget Theme: {settings.widget_theme}")
        print(f"  - Onboarding Enabled: {settings.enable_onboarding}")
        print(f"  - Lead Creation Enabled: {settings.enable_lead_creation}")
        
        return settings
        
    except Exception as e:
        print(f"Error creating AIDA Agent Settings: {str(e)}")
        frappe.log_error(f"Error in setup_aida_settings: {str(e)}", "AIDA Setup")
        raise

if __name__ == "__main__":
    setup_aida_settings()