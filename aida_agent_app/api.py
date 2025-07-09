import frappe
import requests
import json
import logging
import time
from frappe import _
from frappe.utils import get_site_url, validate_email_address
from frappe.rate_limiter import rate_limit

# Configure logging
logger = logging.getLogger(__name__)

@frappe.whitelist()
def get_settings():
    """
    Get AIDA Agent settings from the database.
    """
    try:
        # Try to get existing settings
        settings = frappe.get_single("AIDA Agent Settings")
        return {
            "success": True,
            "settings": {
                "api_server_url": settings.get("api_server_url", "http://localhost:5000"),
                "erpnext_url": settings.get("erpnext_url", get_site_url(frappe.local.site)),
                "google_api_key": settings.get("google_api_key", ""),
                "mongo_uri": settings.get("mongo_uri", ""),
                "enable_onboarding": settings.get("enable_onboarding", 1),
                "enable_lead_creation": settings.get("enable_lead_creation", 1),
                "widget_position": settings.get("widget_position", "bottom-right"),
                "widget_theme": settings.get("widget_theme", "light")
            }
        }
    except Exception as e:
        frappe.log_error(f"Error getting AIDA settings: {str(e)}", "AIDA Agent Settings")
        # Return default settings if document doesn't exist
        return {
            "success": True,
            "settings": {
                "api_server_url": "http://localhost:5000",
                "erpnext_url": get_site_url(frappe.local.site),
                "google_api_key": "",
                "mongo_uri": "",
                "enable_onboarding": 1,
                "enable_lead_creation": 1,
                "widget_position": "bottom-right",
                "widget_theme": "light"
            }
        }

@frappe.whitelist()
@rate_limit(limit=10, seconds=60, methods=["POST"])
def save_settings(settings):
    """
    Save AIDA Agent settings to the database with enhanced validation.
    """
    try:
        if isinstance(settings, str):
            # Validate request size
            if len(settings) > 10000:  # 10KB limit
                frappe.throw("Request payload too large")
            settings = json.loads(settings)
        
        # Validate required fields and formats
        if 'api_server_url' in settings and settings['api_server_url']:
            if not settings['api_server_url'].startswith(('http://', 'https://')):
                frappe.throw("API Server URL must start with http:// or https://")
                
        if 'erpnext_url' in settings and settings['erpnext_url']:
            if not settings['erpnext_url'].startswith(('http://', 'https://')):
                frappe.throw("ERPNext URL must start with http:// or https://")
                
        if 'google_api_key' in settings and settings['google_api_key']:
            if len(settings['google_api_key']) < 20:
                frappe.throw("Invalid Google API key format")
                
        if 'mongo_uri' in settings and settings['mongo_uri']:
            if not settings['mongo_uri'].startswith(('mongodb://', 'mongodb+srv://')):
                frappe.throw("Invalid MongoDB URI format")
        
        # Get or create settings document
        try:
            doc = frappe.get_single("AIDA Agent Settings")
        except frappe.DoesNotExistError:
            doc = frappe.new_doc("AIDA Agent Settings")
        
        # Update settings with validation
        allowed_fields = ['api_server_url', 'erpnext_url', 'google_api_key', 'mongo_uri', 
                         'enable_onboarding', 'enable_lead_creation', 'widget_position', 'widget_theme']
        
        update_data = {}
        for key in allowed_fields:
            if key in settings:
                update_data[key] = settings[key]
            else:
                # Set defaults for missing fields
                defaults = {
                    "api_server_url": "http://localhost:5000",
                    "erpnext_url": get_site_url(frappe.local.site),
                    "google_api_key": "",
                    "mongo_uri": "",
                    "enable_onboarding": 1,
                    "enable_lead_creation": 1,
                    "widget_position": "bottom-right",
                    "widget_theme": "light"
                }
                update_data[key] = defaults.get(key, "")
        
        doc.update(update_data)
        doc.save()
        frappe.db.commit()
        
        logger.info(f"AIDA settings saved by user {frappe.session.user}")
        return {"success": True, "message": "Settings saved successfully"}
        
    except Exception as e:
        logger.error(f"Error saving AIDA settings: {str(e)}", exc_info=True)
        frappe.log_error(f"Error saving AIDA settings: {str(e)}", "AIDA Agent Settings")
        return {"success": False, "message": f"Error saving settings: {str(e)}"}

@frappe.whitelist()
def test_connection():
    """
    Test connection to AIDA API server.
    """
    try:
        settings = get_settings()
        if not settings["success"]:
            return {"success": False, "message": "Could not load settings"}
        
        api_server_url = settings["settings"]["api_server_url"]
        
        # Test health endpoint
        response = requests.get(f"{api_server_url}/health", timeout=10)
        
        if response.status_code == 200:
            return {
                "success": True, 
                "message": "Connection successful",
                "server_status": response.json()
            }
        else:
            return {
                "success": False, 
                "message": f"Server returned status code: {response.status_code}"
            }
            
    except requests.exceptions.RequestException as e:
        return {
            "success": False, 
            "message": f"Connection failed: {str(e)}"
        }
    except Exception as e:
        frappe.log_error(f"Error testing AIDA connection: {str(e)}", "AIDA Agent Connection Test")
        return {
            "success": False, 
            "message": f"Unexpected error: {str(e)}"
        }

@frappe.whitelist()
def init_agent_session():
    """
    Initialize a new AIDA agent session.
    """
    try:
        settings = get_settings()
        if not settings["success"]:
            return {"success": False, "message": "Could not load settings"}
        
        settings_data = settings["settings"]
        api_server_url = settings_data["api_server_url"]
        
        # Get current user session info
        user = frappe.session.user
        sid = frappe.session.sid
        
        payload = {
            "erpnext_url": settings_data["erpnext_url"],
            "username": user,
            "password": "session_token",
            "google_api_key": settings_data["google_api_key"],
            "mongo_uri": settings_data["mongo_uri"],
            "site_base_url": settings_data["erpnext_url"],
            "api_key": user,
            "api_secret": sid
        }
        
        response = requests.post(
            f"{api_server_url}/init_session",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "session_data": response.json()
            }
        else:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
            return {
                "success": False,
                "message": error_data.get("error", f"Failed to initialize session: {response.status_code}")
            }
            
    except Exception as e:
        frappe.log_error(f"Error initializing AIDA session: {str(e)}", "AIDA Agent Session")
        return {
            "success": False,
            "message": f"Failed to initialize session: {str(e)}"
        }

@frappe.whitelist()
@rate_limit(limit=20, seconds=60, methods=["POST"])
def chat_with_agent(session_id, user_input):
    """
    Send a message to the AIDA agent with enhanced security.
    """
    start_time = time.time()
    
    try:
        # Enhanced input validation
        if not user_input or not isinstance(user_input, str):
            return {"success": False, "message": "Valid message is required"}
            
        user_input = user_input.strip()
        if len(user_input) > 1000:  # Limit message length
            return {"success": False, "message": "Message too long (max 1000 characters)"}
            
        # Sanitize input (basic XSS prevention)
        user_input = frappe.utils.sanitize_html(user_input)
        
        if not session_id:
            return {"success": False, "message": "Session ID is required"}
        
        settings = get_settings()
        if not settings["success"]:
            return {"success": False, "message": "Could not load settings"}
        
        api_server_url = settings["settings"]["api_server_url"]
        
        payload = {
            "session_id": session_id,
            "user_input": user_input,
            "user": frappe.session.user,
            "site": get_site_url(frappe.local.site)
        }
        
        # Send request with retry logic
        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                response = requests.post(
                    f"{api_server_url}/chat",
                    json=payload,
                    timeout=60,
                    headers={'Content-Type': 'application/json'}
                )
                break
            except requests.exceptions.RequestException as e:
                if attempt == max_retries:
                    raise e
                time.sleep(1)  # Wait before retry
        
        duration = time.time() - start_time
        
        if response.status_code == 200:
            logger.info(f"AIDA chat request completed in {duration:.2f}s for user {frappe.session.user}")
            return {
                "success": True,
                "response_data": response.json()
            }
        else:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
            logger.warning(f"AIDA API returned status {response.status_code}")
            return {
                "success": False,
                "message": error_data.get("error", f"Chat failed: {response.status_code}")
            }
            
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Error in AIDA chat after {duration:.2f}s: {str(e)}", exc_info=True)
        frappe.log_error(f"Error in AIDA chat: {str(e)}", "AIDA Agent Chat")
        return {
            "success": False,
            "message": "An error occurred while processing your request"
        }

@frappe.whitelist()
def create_leads(business_type, location, count=10):
    """
    Create leads using the separated lead creation endpoint.
    """
    try:
        settings = get_settings()
        if not settings["success"]:
            return {"success": False, "message": "Could not load settings"}
        
        settings_data = settings["settings"]
        api_server_url = settings_data["api_server_url"]
        
        # Get current user session info
        user = frappe.session.user
        sid = frappe.session.sid
        
        payload = {
            "erpnext_url": settings_data["erpnext_url"],
            "username": user,
            "password": sid,
            "google_api_key": settings_data["google_api_key"],
            "business_type": business_type,
            "location": location,
            "count": int(count)
        }
        
        response = requests.post(
            f"{api_server_url}/create_leads",
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "result": response.json()
            }
        else:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
            return {
                "success": False,
                "message": error_data.get("error", f"Lead creation failed: {response.status_code}")
            }
            
    except Exception as e:
        frappe.log_error(f"Error creating leads: {str(e)}", "AIDA Lead Creation")
        return {
            "success": False,
            "message": f"Lead creation failed: {str(e)}"
        }

@frappe.whitelist()
def clear_agent_session(session_id):
    """
    Clear an AIDA agent session.
    """
    try:
        settings = get_settings()
        if not settings["success"]:
            return {"success": False, "message": "Could not load settings"}
        
        api_server_url = settings["settings"]["api_server_url"]
        
        payload = {"session_id": session_id}
        
        response = requests.post(
            f"{api_server_url}/clear_session",
            json=payload,
            timeout=10
        )
        
        return {
            "success": response.status_code == 200,
            "message": "Session cleared" if response.status_code == 200 else "Failed to clear session"
        }
        
    except Exception as e:
        frappe.log_error(f"Error clearing AIDA session: {str(e)}", "AIDA Agent Session")
        return {
            "success": False,
            "message": f"Failed to clear session: {str(e)}"
        }