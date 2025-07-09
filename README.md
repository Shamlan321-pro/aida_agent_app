# AIDA Agent App for ERPNext

An intelligent AI-powered assistant app for ERPNext that provides onboarding guidance and automated lead generation capabilities.

## Features

### 🎯 Intelligent Onboarding
- **Smart Q&A Detection**: Automatically detects "how-to" questions and provides step-by-step guidance
- **Contextual Help**: Generates clickable links to relevant ERPNext forms and views
- **DocType Discovery**: Automatically discovers and suggests relevant doctypes for user queries
- **Interactive Guidance**: Provides comprehensive instructions for common ERPNext operations

### 🚀 Lead Generation
- **Google Maps Integration**: Search for businesses using Google Places API
- **Automated Lead Creation**: Convert business search results into ERPNext leads
- **Bulk Processing**: Handle multiple leads efficiently
- **Smart Filtering**: Filter and validate leads before creation

### 💬 Chat Interface
- **Floating Chat Widget**: Unobtrusive chat interface accessible from any ERPNext page
- **Session Management**: Persistent chat sessions with conversation history
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Dark/Light Theme**: Automatic theme detection and switching

## Installation

### Prerequisites
- ERPNext v14.0.0 or higher
- Python 3.8 or higher
- AIDA API Server running (see main project)

### Step 1: Install the App

```bash
# Navigate to your Frappe bench directory
cd /path/to/your/frappe-bench

# Get the app
bench get-app aida_agent_app /path/to/aida_taskforge_agent-main/aida_agent_app

# Install on your site
bench --site your-site-name install-app aida_agent_app
```

### Step 2: Configure Settings

1. Go to **Setup > AIDA Agent Settings**
2. Configure the following:
   - **API Server URL**: URL of your AIDA API server (e.g., `http://localhost:8000`)
   - **ERPNext URL**: Your ERPNext site URL
   - **Google API Key**: For lead generation (optional)
   - **MongoDB URI**: For session storage (optional)

3. Enable desired features:
   - **Enable Onboarding**: Turn on intelligent Q&A assistance
   - **Enable Lead Creation**: Turn on lead generation capabilities

4. Test the connection using the "Test Connection" button

### Step 3: Start AIDA API Server

Make sure the AIDA API server is running:

```bash
cd /path/to/aida_taskforge_agent-main
python aida_api_server.py
```

## Usage

### Chat Interface

Once installed and configured, you'll see a floating chat button on all ERPNext pages. Click it to:

- Ask "how-to" questions about ERPNext operations
- Get step-by-step guidance with clickable links
- Generate leads from business searches
- Get contextual help for your current page

### Example Queries

**Onboarding Questions:**
- "How do I create a new customer?"
- "How to make a sales invoice?"
- "How do I set up a new item?"
- "How to create a purchase order?"

**Lead Generation:**
- "Find restaurants in New York"
- "Search for tech companies in San Francisco"
- "Generate leads for retail stores in Chicago"

### API Endpoints

The app provides several API endpoints for integration:

- `GET /api/method/aida_agent_app.api.get_settings` - Get current settings
- `POST /api/method/aida_agent_app.api.save_settings` - Save settings
- `POST /api/method/aida_agent_app.api.test_connection` - Test API connection
- `POST /api/method/aida_agent_app.api.init_agent_session` - Initialize chat session
- `POST /api/method/aida_agent_app.api.chat_with_agent` - Send chat message
- `POST /api/method/aida_agent_app.api.create_leads` - Generate leads
- `POST /api/method/aida_agent_app.api.clear_agent_session` - Clear session

## Configuration Options

### Widget Settings
- **Position**: Choose chat widget position (bottom-right, bottom-left, etc.)
- **Theme**: Auto, light, or dark theme
- **Size**: Compact or expanded chat window

### Feature Toggles
- **Onboarding**: Enable/disable intelligent Q&A assistance
- **Lead Creation**: Enable/disable lead generation features
- **Session Persistence**: Enable/disable conversation history

### API Configuration
- **Rate Limiting**: Configure request limits per IP
- **Timeout Settings**: Adjust API timeout values
- **Retry Logic**: Configure retry attempts for failed requests

## Troubleshooting

### Common Issues

**Chat widget not appearing:**
- Check if the app is installed: `bench --site your-site list-apps`
- Verify settings are configured correctly
- Check browser console for JavaScript errors

**Connection test failing:**
- Ensure AIDA API server is running
- Check firewall settings
- Verify API server URL is correct

**Lead generation not working:**
- Verify Google API key is valid
- Check API key has Places API enabled
- Ensure sufficient API quota

### Debug Mode

Enable debug mode in settings to see detailed logs:

```javascript
// In browser console
localStorage.setItem('aida_debug', 'true');
```

### Log Files

Check ERPNext error logs:
```bash
tail -f /path/to/frappe-bench/logs/your-site-name.error.log
```

## Development

### File Structure
```
aida_agent_app/
├── aida_agent_app/
│   ├── api.py                 # API endpoints
│   ├── doctype/
│   │   └── aida_agent_settings/
│   │       ├── aida_agent_settings.json
│   │       ├── aida_agent_settings.py
│   │       └── aida_agent_settings.js
│   ├── public/
│   │   ├── css/
│   │   │   └── aida_agent.css
│   │   └── js/
│   │       └── aida_agent.js
│   └── config/
│       └── desktop.py
├── hooks.py                   # App configuration
├── __init__.py
├── __version__.py
└── requirements.txt
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For support and questions:
- GitHub Issues: [Create an issue](https://github.com/aida-ai/aida-taskforge-agent/issues)
- Email: support@aida-ai.com
- Documentation: [Full Documentation](https://github.com/aida-ai/aida-taskforge-agent)