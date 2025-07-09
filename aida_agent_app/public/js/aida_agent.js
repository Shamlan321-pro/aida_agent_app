// AIDA Agent App JavaScript

class AidaAgent {
    constructor() {
        this.sessionId = null;
        this.isInitialized = false;
        this.settings = {};
        this.isLoading = false;
        this.messageHistory = [];
        this.messageCache = new Map();
        this.retryCount = 0;
        this.maxRetries = 3;
        this.debounceTimer = null;
        this.debounceDelay = 300;
        
        this.init();
    }
    
    async init() {
        try {
            // Load settings
            await this.loadSettings();
            
            // Create widget
            this.createWidget();
            
            // Initialize session
            await this.initSession();
            
            console.log('AIDA Agent initialized successfully');
        } catch (error) {
            console.error('Failed to initialize AIDA Agent:', error);
        }
    }
    
    async loadSettings() {
        try {
            const response = await frappe.call({
                method: 'aida_agent_app.aida_agent_app.api.get_settings'
            });
            
            if (response.message && response.message.success) {
                this.settings = response.message.settings;
            } else {
                throw new Error('Failed to load settings');
            }
        } catch (error) {
            console.error('Error loading settings:', error);
            // Use default settings
            this.settings = {
                api_server_url: 'http://localhost:5000',
                erpnext_url: window.location.origin,
                enable_onboarding: 1,
                enable_lead_creation: 1,
                widget_position: 'bottom-right',
                widget_theme: 'light'
            };
        }
    }
    
    createWidget() {
        // Remove existing widget if any
        const existingWidget = document.getElementById('aida-chat-widget');
        if (existingWidget) {
            existingWidget.remove();
        }
        
        // Create widget HTML
        const widgetHTML = `
            <div id="aida-chat-widget" class="aida-chat-widget ${this.settings.widget_position} ${this.settings.widget_theme}">
                <button class="aida-chat-button" id="aida-chat-toggle">
                    <i class="fa fa-comments"></i>
                </button>
                
                <div class="aida-chat-window" id="aida-chat-window">
                    <div class="aida-chat-header">
                        <h3>AIDA AI Assistant</h3>
                        <button class="close-btn" id="aida-chat-close">
                            <i class="fa fa-times"></i>
                        </button>
                    </div>
                    
                    <div class="aida-chat-messages" id="aida-chat-messages">
                        <div class="aida-message bot">
                            <div class="aida-message-content">
                                Hello! I'm AIDA, your AI assistant. I can help you with:
                                <br>• Creating and managing ERPNext records
                                <br>• Step-by-step guidance for any task
                                <br>• Lead generation and outreach
                                <br><br>How can I assist you today?
                            </div>
                        </div>
                    </div>
                    
                    <div class="aida-chat-input">
                        <input type="text" id="aida-message-input" placeholder="Type your message..." maxlength="2000">
                        <button id="aida-send-button">
                            <i class="fa fa-paper-plane"></i>
                        </button>
                    </div>
                </div>
                
                <!-- Lead Creation Panel -->
                <div class="aida-lead-panel" id="aida-lead-panel">
                    <div class="aida-lead-panel-header">
                        <h3>Lead Generation</h3>
                        <button class="close-btn" id="aida-lead-close">
                            <i class="fa fa-times"></i>
                        </button>
                    </div>
                    
                    <div class="aida-lead-panel-content">
                        <div id="aida-lead-alerts"></div>
                        
                        <div class="aida-form-group">
                            <label for="business-type">Business Type</label>
                            <input type="text" id="business-type" placeholder="e.g., restaurants, law firms, dentists">
                        </div>
                        
                        <div class="aida-form-group">
                            <label for="location">Location</label>
                            <input type="text" id="location" placeholder="e.g., New York, NY">
                        </div>
                        
                        <div class="aida-form-group">
                            <label for="lead-count">Number of Leads</label>
                            <select id="lead-count">
                                <option value="5">5 leads</option>
                                <option value="10" selected>10 leads</option>
                                <option value="20">20 leads</option>
                                <option value="50">50 leads</option>
                            </select>
                        </div>
                        
                        <button class="aida-btn" id="create-leads-btn">
                            <i class="fa fa-users"></i> Create Leads
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        // Add widget to page
        document.body.insertAdjacentHTML('beforeend', widgetHTML);
        
        // Add event listeners
        this.addEventListeners();
    }
    
    addEventListeners() {
        // Chat toggle
        document.getElementById('aida-chat-toggle').addEventListener('click', () => {
            this.toggleChat();
        });
        
        // Chat close
        document.getElementById('aida-chat-close').addEventListener('click', () => {
            this.closeChat();
        });
        
        // Send message
        document.getElementById('aida-send-button').addEventListener('click', () => {
            this.sendMessage();
        });
        
        // Enhanced input handling with debouncing
        const messageInput = document.getElementById('aida-message-input');
        
        // Debounced input validation
        messageInput.addEventListener('input', (e) => {
            clearTimeout(this.debounceTimer);
            this.debounceTimer = setTimeout(() => {
                this.validateInput(e.target.value);
            }, this.debounceDelay);
        });
        
        // Enter key to send
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Add focus management for accessibility
        messageInput.addEventListener('focus', () => {
            document.getElementById('aida-chat-widget').classList.add('aida-focused');
        });
        
        messageInput.addEventListener('blur', () => {
            document.getElementById('aida-chat-widget').classList.remove('aida-focused');
        });
        
        // Lead panel close
        document.getElementById('aida-lead-close').addEventListener('click', () => {
            this.closeLeadPanel();
        });
        
        // Create leads
        document.getElementById('create-leads-btn').addEventListener('click', () => {
            this.createLeads();
        });
    }
    
    async initSession() {
        try {
            const response = await frappe.call({
                method: 'aida_agent_app.aida_agent_app.api.init_agent_session'
            });
            
            if (response.message && response.message.success) {
                this.sessionId = response.message.session_data.session_id;
                this.isInitialized = true;
                console.log('AIDA session initialized:', this.sessionId);
            } else {
                throw new Error(response.message?.message || 'Failed to initialize session');
            }
        } catch (error) {
            console.error('Session initialization failed:', error);
            this.showError('Failed to connect to AIDA AI. Please check your settings.');
        }
    }
    
    toggleChat() {
        const chatWindow = document.getElementById('aida-chat-window');
        const chatButton = document.getElementById('aida-chat-toggle');
        
        if (chatWindow.classList.contains('show')) {
            this.closeChat();
        } else {
            chatWindow.classList.add('show');
            chatButton.classList.add('active');
            document.getElementById('aida-message-input').focus();
        }
    }
    
    closeChat() {
        const chatWindow = document.getElementById('aida-chat-window');
        const chatButton = document.getElementById('aida-chat-toggle');
        
        chatWindow.classList.remove('show');
        chatButton.classList.remove('active');
    }
    
    openLeadPanel() {
        document.getElementById('aida-lead-panel').classList.add('show');
    }
    
    closeLeadPanel() {
        document.getElementById('aida-lead-panel').classList.remove('show');
    }
    
    async sendMessage() {
        const input = document.getElementById('aida-message-input');
        const message = input.value.trim();
        
        if (!message || this.isLoading) return;
        
        if (!this.isInitialized) {
            this.showError('AIDA is not connected. Please refresh the page.');
            return;
        }
        
        // Check cache first
        const cacheKey = message.toLowerCase().trim();
        if (this.messageCache.has(cacheKey)) {
            const cachedResponse = this.messageCache.get(cacheKey);
            input.value = '';
            this.addMessage(message, 'user');
            this.addMessage(cachedResponse, 'bot');
            return;
        }
        
        // Clear input
        input.value = '';
        
        // Add user message
        this.addMessage(message, 'user');
        
        // Check for lead creation intent
        if (this.isLeadCreationQuery(message)) {
            this.addMessage('I can help you create leads! Let me open the lead generation panel for you.', 'bot');
            setTimeout(() => this.openLeadPanel(), 1000);
            return;
        }
        
        // Show loading
        this.showLoading();
        
        try {
            const response = await this.sendMessageWithRetry(message);
            
            this.hideLoading();
            
            if (response && response.message && response.message.success) {
                const botResponse = response.message.response_data.response;
                this.addMessage(botResponse, 'bot');
                
                // Cache the response
                this.messageCache.set(cacheKey, botResponse);
                
                // Limit cache size
                if (this.messageCache.size > 50) {
                    const firstKey = this.messageCache.keys().next().value;
                    this.messageCache.delete(firstKey);
                }
                
                this.retryCount = 0; // Reset retry count on success
            } else {
                this.handleError('Sorry, I encountered an error. Please try again.');
            }
        } catch (error) {
            this.hideLoading();
            console.error('Chat error:', error);
            this.handleError('Sorry, I\'m having trouble connecting. Please try again later.');
        }
    }
    
    async sendMessageWithRetry(message, attempt = 1) {
        try {
            return await frappe.call({
                method: 'aida_agent_app.aida_agent_app.api.chat_with_agent',
                args: {
                    session_id: this.sessionId,
                    user_input: message
                },
                timeout: 30000
            });
        } catch (error) {
            if (attempt < this.maxRetries && this.isRetryableError(error)) {
                console.warn(`Attempt ${attempt} failed, retrying...`, error);
                await this.delay(1000 * attempt); // Exponential backoff
                return this.sendMessageWithRetry(message, attempt + 1);
            }
            throw error;
        }
    }
    
    isRetryableError(error) {
        // Retry on network errors, timeouts, and 5xx server errors
        return error.name === 'NetworkError' || 
               error.message.includes('timeout') ||
               (error.status >= 500 && error.status < 600);
    }
    
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    handleError(message) {
        this.addMessage(message, 'bot');
        this.retryCount++;
        
        if (this.retryCount >= this.maxRetries) {
            this.addMessage('I\'m experiencing persistent issues. Please refresh the page and try again.', 'bot');
        }
    }
    
    isLeadCreationQuery(message) {
        const leadKeywords = [
            'create leads', 'generate leads', 'find leads', 'lead generation',
            'find businesses', 'search businesses', 'prospect', 'prospecting'
        ];
        
        const lowerMessage = message.toLowerCase();
        return leadKeywords.some(keyword => lowerMessage.includes(keyword));
    }
    
    addMessage(content, type) {
        const messagesContainer = document.getElementById('aida-chat-messages');
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `aida-message ${type}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'aida-message-content';
        
        // Process content for clickable links
        if (type === 'bot') {
            contentDiv.innerHTML = this.processMessageContent(content);
        } else {
            contentDiv.textContent = content;
        }
        
        messageDiv.appendChild(contentDiv);
        messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // Store in history
        this.messageHistory.push({ content, type, timestamp: new Date() });
    }
    
    processMessageContent(content) {
        // Convert URLs to clickable links
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        return content.replace(urlRegex, '<a href="$1" target="_blank">$1</a>');
    }
    
    showLoading() {
        this.isLoading = true;
        const messagesContainer = document.getElementById('aida-chat-messages');
        
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'aida-message bot';
        loadingDiv.id = 'aida-loading-message';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'aida-message-content';
        contentDiv.innerHTML = `
            <div class="aida-loading">
                <div class="aida-loading-dot"></div>
                <div class="aida-loading-dot"></div>
                <div class="aida-loading-dot"></div>
            </div>
        `;
        
        loadingDiv.appendChild(contentDiv);
        messagesContainer.appendChild(loadingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // Disable send button
        document.getElementById('aida-send-button').disabled = true;
    }
    
    hideLoading() {
        this.isLoading = false;
        const loadingMessage = document.getElementById('aida-loading-message');
        if (loadingMessage) {
            loadingMessage.remove();
        }
        
        // Enable send button
        document.getElementById('aida-send-button').disabled = false;
    }
    
    async createLeads() {
        const businessType = document.getElementById('business-type').value.trim();
        const location = document.getElementById('location').value.trim();
        const count = document.getElementById('lead-count').value;
        
        if (!businessType || !location) {
            this.showLeadAlert('Please fill in both business type and location.', 'error');
            return;
        }
        
        const createBtn = document.getElementById('create-leads-btn');
        createBtn.disabled = true;
        createBtn.innerHTML = '<i class="fa fa-spinner fa-spin"></i> Creating Leads...';
        
        try {
            const response = await frappe.call({
                method: 'aida_agent_app.aida_agent_app.api.create_leads',
                args: {
                    business_type: businessType,
                    location: location,
                    count: count
                }
            });
            
            if (response.message && response.message.success) {
                const result = response.message.result;
                this.showLeadAlert(
                    `Successfully created ${result.result?.created_count || count} leads!`,
                    'success'
                );
                
                // Clear form
                document.getElementById('business-type').value = '';
                document.getElementById('location').value = '';
                
                // Close panel after delay
                setTimeout(() => this.closeLeadPanel(), 2000);
            } else {
                throw new Error(response.message?.message || 'Failed to create leads');
            }
        } catch (error) {
            console.error('Lead creation error:', error);
            this.showLeadAlert(
                `Failed to create leads: ${error.message}`,
                'error'
            );
        } finally {
            createBtn.disabled = false;
            createBtn.innerHTML = '<i class="fa fa-users"></i> Create Leads';
        }
    }
    
    showLeadAlert(message, type) {
        const alertsContainer = document.getElementById('aida-lead-alerts');
        
        const alertDiv = document.createElement('div');
        alertDiv.className = `aida-alert ${type}`;
        alertDiv.textContent = message;
        
        alertsContainer.innerHTML = '';
        alertsContainer.appendChild(alertDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
    
    validateInput(value) {
        const sendBtn = document.getElementById('aida-send-button');
        const input = document.getElementById('aida-message-input');
        
        if (value.trim().length === 0) {
            sendBtn.disabled = true;
            sendBtn.classList.add('disabled');
        } else if (value.length > 2000) {
            input.setCustomValidity('Message too long (max 2000 characters)');
            sendBtn.disabled = true;
            sendBtn.classList.add('disabled');
        } else {
            input.setCustomValidity('');
            sendBtn.disabled = false;
            sendBtn.classList.remove('disabled');
        }
    }
    
    showError(message) {
        this.addMessage(`Error: ${message}`, 'bot');
    }
    
    // Public methods for external access
    openChat() {
        const chatWindow = document.getElementById('aida-chat-window');
        if (!chatWindow.classList.contains('show')) {
            this.toggleChat();
        }
    }
    
    sendQuickMessage(message) {
        const input = document.getElementById('aida-message-input');
        input.value = message;
        this.sendMessage();
    }
}

// Initialize AIDA Agent when page loads
let aidaAgent;

frappe.ready(() => {
    // Only initialize in desk (not in website)
    if (frappe.boot && frappe.boot.user && frappe.boot.user.name !== 'Guest') {
        aidaAgent = new AidaAgent();
        
        // Make it globally accessible
        window.aidaAgent = aidaAgent;
    }
});

// Expose utility functions
window.openAidaChat = function() {
    if (window.aidaAgent) {
        window.aidaAgent.openChat();
    }
};

window.sendAidaMessage = function(message) {
    if (window.aidaAgent) {
        window.aidaAgent.openChat();
        setTimeout(() => {
            window.aidaAgent.sendQuickMessage(message);
        }, 500);
    }
};

window.openAidaLeads = function() {
    if (window.aidaAgent) {
        window.aidaAgent.openLeadPanel();
    }
};