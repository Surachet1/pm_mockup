# Copyright 2019 Bluesystem Technology Co., Ltd (http://bluesystem.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    'name': 'Sales Invoice Plan',
    'summary': 'Add to sales order, ability to manage future invoice plan',
    'version': '10.0.2.0.0',
    'author': 'Bluesystem technology co.,ltd',
    'license': 'AGPL-3',
    'website': '',
    'category': 'Sales',
    'depends': ['account',
                'sale',
                'sale_stock',
                'bst_sale_stock',
                'bst_account_order_type',
                'scm_sale_order',
                'bst_sale_partial_invoice',
                ],
    'data': [
        'data/decimal_data.xml',
        'security/ir.model.access.csv',
        'wizard/sale_create_invoice_plan_view.xml',
        'wizard/sale_make_planned_invoice_view.xml',
        'views/sale_view.xml'
    ],
    'installable': True,
    'development_status': 'alpha',
    'maintainers': ['krittapak A.'],
}
