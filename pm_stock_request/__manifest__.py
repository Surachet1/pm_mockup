# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Trinity Roots :: PM - Stock Request",
    "summary": "Stock",
    "version": "10.0.1.0.0",
    "category": "Stock",
    "description": """

This module for Stock Request.
===========================================================


    """,
    "website": "http://www.trinityroots.co.th/",
    "author": "Trinity Roots",
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        'base',
        'stock',
        'project',
    ],
    'data': [
        'wizard/stock_request_wizard_view.xml',
        'wizard/stock_purchase_wizard_view.xml',
        'views/stock_request_view.xml',
    ],
}
