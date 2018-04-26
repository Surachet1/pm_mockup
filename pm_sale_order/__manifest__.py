# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Trinity Roots :: PM - Sale",
    "summary": "Sale",
    "version": "10.0.1.0.0",
    "category": "Sale",
    "description": """

This module for Project.
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
        'sale',
        'website_quote',
    ],
    'data': [
        'views/sale_views.xml',
    ],
}
