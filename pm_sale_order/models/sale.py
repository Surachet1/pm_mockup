# -*- coding: utf-8 -*-
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
    department = fields.Selection([
        ('om', 'OM'),
        ('hc', 'HC'),
        ('bc', 'BC'),
    ],
    string="หน่วยงาน")
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
    project_sale_id = fields.Many2one(
        'project.project',
        'Project'
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

    @api.onchange('template_id')
    def onchange_template_id(self):
        if not self.template_id:
            return
        template = self.template_id.with_context(lang=self.partner_id.lang)

        order_lines = [(5, 0, 0)]
        for line in template.quote_line:
            discount = 0
            if self.pricelist_id:
                price = self.pricelist_id.with_context(uom=line.product_uom_id.id).get_product_price(line.product_id, 1, False)
                if self.pricelist_id.discount_policy == 'without_discount' and line.price_unit:
                    discount = (line.price_unit - price) / line.price_unit * 100
                    price = line.price_unit

            else:
                price = line.price_unit

            data = {
                'name': line.name,
                'price_unit': price,
                #'discount': 100 - ((100 - discount) * (100 - line.discount)/100),
                'product_qty': line.product_uom_qty,
                'product_id': line.product_id.id,
                #'layout_category_id': line.layout_category_id,
                #'product_uom': line.product_uom_id.id,
                #'website_description': line.website_description,
                #'state': 'draft',
                #'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
            }
            #if self.pricelist_id:
            #    data.update(self.env['sale.order.line']._get_purchase_price(self.pricelist_id, line.product_id, line.product_uom_id, fields.Date.context_today(self)))
            order_lines.append((0, 0, data))

        #self.order_line = order_lines
        #self.order_line._compute_tax_id()
        self.line_cost_ids = order_lines

       #option_lines = []
       #for option in template.options:
       #    if self.pricelist_id:
       #        price = self.pricelist_id.with_context(uom=option.uom_id.id).get_product_price(option.product_id, 1, False)
       #    else:
       #        price = option.price_unit
       #    data = {
       #        'product_id': option.product_id.id,
       #        'layout_category_id': option.layout_category_id,
       #        'name': option.name,
       #        'quantity': option.quantity,
       #        'uom_id': option.uom_id.id,
       #        'price_unit': price,
       #        'discount': option.discount,
       #        'website_description': option.website_description,
       #    }
       #    option_lines.append((0, 0, data))
       #self.options = option_lines

       #if template.number_of_days > 0:
       #    self.validity_date = fields.Date.to_string(datetime.now() + timedelta(template.number_of_days))

       #self.website_description = template.website_description
       #self.require_payment = template.require_payment

       #if template.note:
       #    self.note = template.note


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
