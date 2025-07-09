import unittest
import json
from unittest.mock import patch, MagicMock
import frappe
from aida_agent_app.api import get_settings, save_settings, test_connection, chat_with_agent

class TestAidaAgentAPI(unittest.TestCase):
    """Test cases for AIDA Agent API functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_settings = {
            "api_server_url": "http://localhost:5000",
            "erpnext_url": "http://localhost:8000",
            "google_api_key": "test_google_api_key_12345",
            "mongo_uri": "mongodb://localhost:27017/test",
            "enable_onboarding": 1,
            "enable_lead_creation": 1,
            "widget_position": "bottom-right",
            "widget_theme": "light"
        }
    
    @patch('aida_agent_app.api.frappe.get_single')
    @patch('aida_agent_app.api.get_site_url')
    def test_get_settings_success(self, mock_get_site_url, mock_get_single):
        """Test successful retrieval of settings."""
        mock_get_site_url.return_value = "http://localhost:8000"
        mock_settings = MagicMock()
        mock_settings.get.side_effect = lambda key, default=None: self.test_settings.get(key, default)
        mock_get_single.return_value = mock_settings
        
        result = get_settings()
        
        self.assertTrue(result["success"])
        self.assertIn("settings", result)
        self.assertEqual(result["settings"]["api_server_url"], "http://localhost:5000")
    
    @patch('aida_agent_app.api.frappe.get_single')
    @patch('aida_agent_app.api.get_site_url')
    def test_get_settings_exception(self, mock_get_site_url, mock_get_single):
        """Test get_settings when document doesn't exist."""
        mock_get_site_url.return_value = "http://localhost:8000"
        mock_get_single.side_effect = Exception("Document not found")
        
        result = get_settings()
        
        self.assertTrue(result["success"])
        self.assertEqual(result["settings"]["api_server_url"], "http://localhost:5000")
    
    @patch('aida_agent_app.api.frappe.get_single')
    @patch('aida_agent_app.api.frappe.new_doc')
    @patch('aida_agent_app.api.frappe.db.commit')
    @patch('aida_agent_app.api.logger')
    def test_save_settings_success(self, mock_logger, mock_commit, mock_new_doc, mock_get_single):
        """Test successful saving of settings."""
        mock_doc = MagicMock()
        mock_get_single.return_value = mock_doc
        
        with patch('aida_agent_app.api.frappe.session') as mock_session:
            mock_session.user = "test@example.com"
            result = save_settings(json.dumps(self.test_settings))
        
        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Settings saved successfully")
        mock_doc.update.assert_called_once()
        mock_doc.save.assert_called_once()
        mock_commit.assert_called_once()
    
    @patch('aida_agent_app.api.frappe.throw')
    def test_save_settings_invalid_url(self, mock_throw):
        """Test save_settings with invalid URL format."""
        invalid_settings = self.test_settings.copy()
        invalid_settings["api_server_url"] = "invalid-url"
        
        mock_throw.side_effect = frappe.ValidationError("API Server URL must start with http:// or https://")
        
        with self.assertRaises(frappe.ValidationError):
            save_settings(json.dumps(invalid_settings))
    
    @patch('aida_agent_app.api.frappe.throw')
    def test_save_settings_invalid_google_key(self, mock_throw):
        """Test save_settings with invalid Google API key."""
        invalid_settings = self.test_settings.copy()
        invalid_settings["google_api_key"] = "short"
        
        mock_throw.side_effect = frappe.ValidationError("Invalid Google API key format")
        
        with self.assertRaises(frappe.ValidationError):
            save_settings(json.dumps(invalid_settings))
    
    @patch('aida_agent_app.api.frappe.throw')
    def test_save_settings_large_payload(self, mock_throw):
        """Test save_settings with oversized payload."""
        large_payload = "x" * 15000  # Exceeds 10KB limit
        
        mock_throw.side_effect = frappe.ValidationError("Request payload too large")
        
        with self.assertRaises(frappe.ValidationError):
            save_settings(large_payload)
    
    @patch('aida_agent_app.api.requests.get')
    @patch('aida_agent_app.api.get_settings')
    def test_connection_success(self, mock_get_settings, mock_requests_get):
        """Test successful connection test."""
        mock_get_settings.return_value = {
            "success": True,
            "settings": self.test_settings
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "healthy"}
        mock_requests_get.return_value = mock_response
        
        result = test_connection()
        
        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Connection successful")
        self.assertIn("server_status", result)
    
    @patch('aida_agent_app.api.requests.get')
    @patch('aida_agent_app.api.get_settings')
    def test_connection_failure(self, mock_get_settings, mock_requests_get):
        """Test connection test failure."""
        mock_get_settings.return_value = {
            "success": True,
            "settings": self.test_settings
        }
        
        mock_requests_get.side_effect = Exception("Connection refused")
        
        result = test_connection()
        
        self.assertFalse(result["success"])
        self.assertIn("Connection failed", result["message"])
    
    @patch('aida_agent_app.api.requests.post')
    @patch('aida_agent_app.api.get_settings')
    @patch('aida_agent_app.api.frappe.utils.sanitize_html')
    @patch('aida_agent_app.api.logger')
    def test_chat_with_agent_success(self, mock_logger, mock_sanitize, mock_get_settings, mock_requests_post):
        """Test successful chat with agent."""
        mock_get_settings.return_value = {
            "success": True,
            "settings": self.test_settings
        }
        
        mock_sanitize.return_value = "Hello, how can I help?"
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "I can help you with that!"}
        mock_requests_post.return_value = mock_response
        
        with patch('aida_agent_app.api.frappe.session') as mock_session:
            mock_session.user = "test@example.com"
            result = chat_with_agent("session123", "Hello, how can I help?")
        
        self.assertTrue(result["success"])
        self.assertIn("response_data", result)
    
    def test_chat_with_agent_invalid_input(self):
        """Test chat with agent with invalid input."""
        # Test empty message
        result = chat_with_agent("session123", "")
        self.assertFalse(result["success"])
        self.assertIn("Valid message is required", result["message"])
        
        # Test None message
        result = chat_with_agent("session123", None)
        self.assertFalse(result["success"])
        self.assertIn("Valid message is required", result["message"])
        
        # Test long message
        long_message = "x" * 1001
        result = chat_with_agent("session123", long_message)
        self.assertFalse(result["success"])
        self.assertIn("Message too long", result["message"])
        
        # Test missing session ID
        result = chat_with_agent("", "Hello")
        self.assertFalse(result["success"])
        self.assertIn("Session ID is required", result["message"])
    
    @patch('aida_agent_app.api.requests.post')
    @patch('aida_agent_app.api.get_settings')
    @patch('aida_agent_app.api.frappe.utils.sanitize_html')
    @patch('aida_agent_app.api.time.sleep')
    def test_chat_with_agent_retry_logic(self, mock_sleep, mock_sanitize, mock_get_settings, mock_requests_post):
        """Test chat with agent retry logic."""
        mock_get_settings.return_value = {
            "success": True,
            "settings": self.test_settings
        }
        
        mock_sanitize.return_value = "Hello"
        
        # First two calls fail, third succeeds
        mock_response_success = MagicMock()
        mock_response_success.status_code = 200
        mock_response_success.json.return_value = {"response": "Success!"}
        
        mock_requests_post.side_effect = [
            Exception("Connection error"),
            Exception("Connection error"),
            mock_response_success
        ]
        
        with patch('aida_agent_app.api.frappe.session') as mock_session:
            mock_session.user = "test@example.com"
            result = chat_with_agent("session123", "Hello")
        
        self.assertTrue(result["success"])
        self.assertEqual(mock_requests_post.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)

if __name__ == '__main__':
    unittest.main()