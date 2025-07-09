# Copyright (c) 2024, AIDA AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests

class AidaAgentSettings(Document):
    def validate(self):
        """Validate the settings before saving."""
        if self.api_server_url and not self.api_server_url.startswith(('http://', 'https://')):
            frappe.throw("API Server URL must start with http:// or https://")
        
        if self.erpnext_url and not self.erpnext_url.startswith(('http://', 'https://')):
            frappe.throw("ERPNext URL must start with http:// or https://")
    
    def test_connection(self):
        """Test connection to AIDA API server."""
        try:
            if not self.api_server_url:
                frappe.throw("API Server URL is required")
            
            response = requests.get(f"{self.api_server_url}/health", timeout=10)
            
            if response.status_code == 200:
                server_status = response.json()
                frappe.msgprint(
                    f"Connection successful!<br>"
                    f"Server Status: {server_status.get('status', 'Unknown')}<br>"
                    f"Active Sessions: {server_status.get('active_sessions', 0)}<br>"
                    f"MongoDB Available: {server_status.get('mongodb_available', False)}",
                    title="Connection Test Result",
                    indicator="green"
                )
            else:
                frappe.throw(f"Server returned status code: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            frappe.throw(f"Connection failed: {str(e)}")
        except Exception as e:
            frappe.log_error(f"Error testing AIDA connection: {str(e)}", "AIDA Agent Connection Test")
            frappe.throw(f"Unexpected error: {str(e)}")

@frappe.whitelist()
def test_connection():
    """Test connection from client side."""
    try:
        settings = frappe.get_single("AIDA Agent Settings")
        settings.test_connection()
        return {"success": True, "message": "Connection test completed"}
    except Exception as e:
        return {"success": False, "message": str(e)}