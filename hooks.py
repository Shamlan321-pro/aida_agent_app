app_name = "aida_agent_app"
app_title = "AIDA Agent App"
app_publisher = "AIDA AI"
app_description = "Full AIDA AI Agent with Onboarding and Lead Generation"
app_email = "support@aida-ai.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/aida_agent_app/css/aida_agent.css"
app_include_js = "/assets/aida_agent_app/js/aida_agent.js"

# include js, css files in header of web template
web_include_css = "/assets/aida_agent_app/css/aida_agent.css"
web_include_js = "/assets/aida_agent_app/js/aida_agent.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "aida_agent_app/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "aida_agent_app.utils.jinja_methods",
#	"filters": "aida_agent_app.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "aida_agent_app.install.before_install"
# after_install = "aida_agent_app.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "aida_agent_app.uninstall.before_uninstall"
# after_uninstall = "aida_agent_app.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "aida_agent_app.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"aida_agent_app.tasks.all"
#	],
#	"daily": [
#		"aida_agent_app.tasks.daily"
#	],
#	"hourly": [
#		"aida_agent_app.tasks.hourly"
#	],
#	"weekly": [
#		"aida_agent_app.tasks.weekly"
#	],
#	"monthly": [
#		"aida_agent_app.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "aida_agent_app.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "aida_agent_app.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "aida_agent_app.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["aida_agent_app.utils.before_request"]
# after_request = ["aida_agent_app.utils.after_request"]

# Job Events
# ----------
# before_job = ["aida_agent_app.utils.before_job"]
# after_job = ["aida_agent_app.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"]
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
# ]

# Boot Session
# -------------
boot_session = "aida_agent_app.boot.boot_session"

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"aida_agent_app.auth.validate"
# ]