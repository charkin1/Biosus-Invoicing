app_name = "biosus_invoicing"
app_title = "Biosus Invoicing"
app_publisher = "Conall Harkin, Biosus Energy Ltd."
app_description = "Sales orders and Milestone-based partial invoicing"
app_email = "conall@biosusenergy.com"
app_license = "mit"
doctype_js = {
    "Project": "public/js/project.js",
    "Quotation": "public/js/quotation_utils.js",
}
# Apps
# ------------------
from .api import quotation_utils

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "biosus_invoicing",
# 		"logo": "/assets/biosus_invoicing/logo.png",
# 		"title": "Biosus Invoicing",
# 		"route": "/biosus_invoicing",
# 		"has_permission": "biosus_invoicing.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "public/grid_layout_override.css"

#app_include_js = "/assets/biosus_invoicing/js/project_invoice.js"

# include js, css files in header of web template
# web_include_css = "/assets/biosus_invoicing/css/biosus_invoicing.css"
# web_include_js = "/assets/biosus_invoicing/js/biosus_invoicing.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "biosus_invoicing/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

#include js in doctype views
#doctype_js = {"quotation" : "public/js/quotation_utils.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "biosus_invoicing/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "biosus_invoicing.utils.jinja_methods",
# 	"filters": "biosus_invoicing.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "biosus_invoicing.install.before_install"
# after_install = "biosus_invoicing.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "biosus_invoicing.uninstall.before_uninstall"
# after_uninstall = "biosus_invoicing.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "biosus_invoicing.utils.before_app_install"
# after_app_install = "biosus_invoicing.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "biosus_invoicing.utils.before_app_uninstall"
# after_app_uninstall = "biosus_invoicing.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "biosus_invoicing.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Purchase Receipt": {
        "before_save": "biosus_invoicing.api.api.set_purchase_order_field",
  		"on_submit": "biosus_invoicing.api.api.notify_po_creator"
  	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"biosus_invoicing.tasks.all"
# 	],
# 	"daily": [
# 		"biosus_invoicing.tasks.daily"
# 	],
# 	"hourly": [
# 		"biosus_invoicing.tasks.hourly"
# 	],
# 	"weekly": [
# 		"biosus_invoicing.tasks.weekly"
# 	],
# 	"monthly": [
# 		"biosus_invoicing.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "biosus_invoicing.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "biosus_invoicing.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "biosus_invoicing.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["biosus_invoicing.utils.before_request"]
# after_request = ["biosus_invoicing.utils.after_request"]

# Job Events
# ----------
# before_job = ["biosus_invoicing.utils.before_job"]
# after_job = ["biosus_invoicing.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"biosus_invoicing.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

