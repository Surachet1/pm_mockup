# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Trinity Roots :: PM - Purchase Order",
    "summary": "Purchase",
    "version": "10.0.1.0.0",
    "category": "Purchase",
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
        'purchase',
    ],
    'data': [
        'views/purchase_view.xml',
    ],
}
