# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Trinity Roots :: PM - CRM Claim",
    "summary": "Claim",
    "version": "10.0.1.0.0",
    "category": "CRM",
    "description": """

This module for CRM Claim.
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
        'crm',
        'sales_team',
    ],
    'data': [
        'views/crm_claim_view.xml',
        'views/partner_view.xml',
        'views/crm_lead_view.xml',
    ],
}
