# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe

def boot_session(bootinfo):
    """
    Boot session for AIDA Agent App.
    Add any session-specific data here.
    """
    try:
        # Only add AIDA-specific boot data if user is logged in
        if frappe.session and frappe.session.user and str(frappe.session.user) != 'Guest':
            # Initialize with default primitive values
            aida_config = {
                'enabled': False,
                'version': '1.0.0',
                'widget_position': 'bottom-right',
                'theme': 'light',
                'onboarding_enabled': True,
                'lead_creation_enabled': True
            }
            
            # Use frappe.db.get_single_value to get individual values instead of the Document object
            try:
                enabled = frappe.db.get_single_value('AIDA Agent Settings', 'enabled')
                if enabled is not None:
                    aida_config['enabled'] = bool(enabled)
                    
                widget_position = frappe.db.get_single_value('AIDA Agent Settings', 'widget_position')
                if widget_position:
                    aida_config['widget_position'] = str(widget_position)
                    
                theme = frappe.db.get_single_value('AIDA Agent Settings', 'theme')
                if theme:
                    aida_config['theme'] = str(theme)
                    
                onboarding_enabled = frappe.db.get_single_value('AIDA Agent Settings', 'onboarding_enabled')
                if onboarding_enabled is not None:
                    aida_config['onboarding_enabled'] = bool(onboarding_enabled)
                    
                lead_creation_enabled = frappe.db.get_single_value('AIDA Agent Settings', 'lead_creation_enabled')
                if lead_creation_enabled is not None:
                    aida_config['lead_creation_enabled'] = bool(lead_creation_enabled)
            except Exception as settings_error:
                # If settings don't exist or can't be retrieved, use defaults
                frappe.log_error(f"Could not retrieve AIDA settings: {str(settings_error)}", "AIDA Settings Error")
            
            # Assign the clean config to bootinfo
            bootinfo['aida_agent'] = aida_config
                
    except Exception as e:
        # Log error but don't break boot process
        try:
            frappe.log_error(f"AIDA Agent boot error: {str(e)}", "AIDA Agent Boot")
        except:
            pass