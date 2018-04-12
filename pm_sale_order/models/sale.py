from odoo import api, fields, models, _, exceptions

class SaleOrder(models.Model):

    _inherit = 'sale.order'
    _description = 'Sale'

    partner_contact_id = fields.Many2one(
        'res.partner',
        string="Contact Customer",
    )
    code = fields.Char(
        "Code"
    )
    partner_invoice_id = fields.Many2one(
        'res.partner',
        string='Invoice Address',
        readonly=True,
        required=True,
        states={
            'draft': [('readonly', False)],
            'sent': [('readonly', False)],
            'approve': [('readonly', False)],
        },
        help="Invoice address for current sales order."
    )
    partner_shipping_id = fields.Many2one(
        'res.partner',
        string='Delivery Address',
        readonly=True,
        required=True,
        states={
            'draft': [('readonly', False)],
            'sent': [('readonly', False)],
            'approve': [('readonly', False)],
        },
        help="Delivery address for current sales order."
    )
    ref = fields.Char(
        "Reference/Description"
    )
    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Warehouse'
    )
    quo_temp = fields.Char(
        "Quote Template"
    )
    pricelist_id = fields.Many2one(
        'product.pricelist',
        'Pricelist',
    )
    contract_no = fields.Char(
        "Cantract NO."
    )
    invoice_no = fields.Char(
        "Invoice NO."
    )
    receipt_no = fields.Char(
        "Receipt NO."
    )
    line_cost_ids = fields.One2many(
        'sale.cost.line',
        'sale_id',
        'Cost Line',
        readonly=False,
        track_visibility='onchange'
    )


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    account_analytic_id = fields.Many2one(
        'account.analytic.account',
        'Analytic Account'
    )
    cost_price = fields.Float(
        'Total Cost Price',
        default=0.0
    )
    margin = fields.Float(
        'Margin',
        default=0.0
    )
    date_start = fields.Datetime(
        string="Start Date",
        required=False,
    )
    date_finishes = fields.Datetime(
        string="Finish Date",
        required=False,
    )
    price_unit = fields.Float(
        'Total Selling Price',
        required=True,
    )

class SaleCostLine(models.Model):

    _name = 'sale.cost.line'

    sale_id = fields.Many2one(
        'sale.order',
        'Sale'
    )
    sale_line_id = fields.Many2one(
        'sale.order.line',
        'Sale Line Parent',
    )
    product_id = fields.Many2one(
        'product.product',
        'Product'
    )
    name = fields.Text(
        'Description',
        size=256,
       track_visibility='onchange'
    )
    product_qty = fields.Float(
        'Quantity'
    )
    cost_price = fields.Float(
        'Product Cost Price',
        default=0.0
    )
    price_unit = fields.Float(
        'Selling Price',
        required=True,
    )
