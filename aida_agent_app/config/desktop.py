from frappe import _

def get_data():
    return [
        {
            "module_name": "AIDA Agent App",
            "color": "#3498db",
            "icon": "fa fa-robot",
            "type": "module",
            "label": _("AIDA Agent"),
            "description": _("AI-powered ERPNext assistant for onboarding and lead generation"),
            "category": "Modules"
        }
    ]