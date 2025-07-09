// Copyright (c) 2024, AIDA AI and contributors
// For license information, please see license.txt

frappe.ui.form.on('AIDA Agent Settings', {
    refresh: function(frm) {
        // Add custom button for testing connection
        frm.add_custom_button(__('Test Connection'), function() {
            test_aida_connection(frm);
        }, __('Actions'));
        
        // Set button style
        frm.page.btn_secondary.find('.btn-default:contains("Test Connection")')
            .removeClass('btn-default').addClass('btn-info');
    },
    
    api_server_url: function(frm) {
        // Validate URL format
        if (frm.doc.api_server_url && !frm.doc.api_server_url.match(/^https?:\/\//)) {
            frappe.msgprint({
                title: __('Invalid URL'),
                message: __('API Server URL must start with http:// or https://'),
                indicator: 'orange'
            });
        }
    },
    
    erpnext_url: function(frm) {
        // Validate URL format
        if (frm.doc.erpnext_url && !frm.doc.erpnext_url.match(/^https?:\/\//)) {
            frappe.msgprint({
                title: __('Invalid URL'),
                message: __('ERPNext URL must start with http:// or https://'),
                indicator: 'orange'
            });
        }
    },
    
    enable_onboarding: function(frm) {
        if (frm.doc.enable_onboarding) {
            frappe.msgprint({
                title: __('Onboarding Enabled'),
                message: __('Users will now see helpful guidance for ERPNext operations'),
                indicator: 'green'
            });
        }
    },
    
    enable_lead_creation: function(frm) {
        if (frm.doc.enable_lead_creation && !frm.doc.google_api_key) {
            frappe.msgprint({
                title: __('Google API Key Required'),
                message: __('Lead creation requires a Google API key for business search'),
                indicator: 'orange'
            });
        }
    }
});

function test_aida_connection(frm) {
    if (!frm.doc.api_server_url) {
        frappe.msgprint({
            title: __('Missing Configuration'),
            message: __('Please enter the API Server URL before testing connection'),
            indicator: 'red'
        });
        return;
    }
    
    frappe.show_alert({
        message: __('Testing connection...'),
        indicator: 'blue'
    });
    
    frappe.call({
        method: 'aida_agent_app.doctype.aida_agent_settings.aida_agent_settings.test_connection',
        callback: function(r) {
            if (r.message && r.message.success) {
                frappe.show_alert({
                    message: __('Connection test completed successfully'),
                    indicator: 'green'
                });
            } else {
                frappe.msgprint({
                    title: __('Connection Test Failed'),
                    message: r.message ? r.message.message : __('Unknown error occurred'),
                    indicator: 'red'
                });
            }
        },
        error: function(r) {
            frappe.msgprint({
                title: __('Connection Test Failed'),
                message: __('Failed to communicate with server'),
                indicator: 'red'
            });
        }
    });
}