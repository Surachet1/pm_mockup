# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Trinity Roots :: PM - Operation",
    "summary": "Operation",
    "version": "10.0.1.0.0",
    "category": "Operation",
    "description": """

This module for Operation OM and HC.
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
    ],
    'data': [
        'views/service_type_view.xml',
        'views/service.xml',
        'views/crm_helpdesk_view.xml',
    ],
}
