import frappe
from frappe import _

def get_context(context):
    """
    Context for AIDA Agent page
    """
    context.title = _("AIDA Agent")
    context.show_sidebar = False
    
    # Check if user is logged in
    if frappe.session.user == "Guest":
        frappe.throw(_("Please login to access AIDA Agent"), frappe.PermissionError)
    
    # Get AIDA Agent settings
    try:
        settings = frappe.get_single("AIDA Agent Settings")
        context.settings = {
            "widget_position": settings.get("widget_position", "bottom-right"),
            "widget_theme": settings.get("widget_theme", "light"),
            "enable_onboarding": settings.get("enable_onboarding", 1),
            "enable_lead_creation": settings.get("enable_lead_creation", 1)
        }
    except:
        # Default settings if document doesn't exist
        context.settings = {
            "widget_position": "bottom-right",
            "widget_theme": "light",
            "enable_onboarding": 1,
            "enable_lead_creation": 1
        }
    
    return context