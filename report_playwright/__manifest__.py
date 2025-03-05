# Copyright 2025 Akretion (http://akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Playwright Report Engine",
    "summary": "Reporting engine based on playwright",
    "version": "16.0.1.0.5",
    "category": "Reporting",
    "license": "AGPL-3",
    "author": "François Poizat, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/reporting-engine",
    "depends": ["web"],
    "external_dependencies": {
        "python": ["playwright"],
    },
    "assets": {
        "web.assets_backend": [
            "report_playwright/static/src/js/playwright_action_service.esm.js",
        ],
    },
    "data": [],
    "installable": True,
}
