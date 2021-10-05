# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero


class SaleInvoiceSelect(models.TransientModel):
    _inherit = "sale.invoice.select"

    def _get_line_sale(self, obj):
        line_sale = []
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        for line in obj.order_line:
            #if line.qty_to_invoice > 0:
            #if float_is_zero(line.qty_to_invoice, precision_digits=precision):
            #    continue
            #qty = line.qty_to_invoice
            qty = line.qty_delivered - line.qty_invoiced
            if obj.use_invoice_plan:
                qty = line.qty_delivered
            if float_is_zero(qty, precision_digits=precision):
                continue
            analytic = line.account_analytic_id.id
            if qty < 0:
                analytic = False
            line_sale.append((0, 0, {
                'sale_line_id': line.id,
                'product_id': line.product_id.id,
                'name': line.name,
                'product_uom_qty': qty,
                'product_uom': line.product_uom.id,
                'account_analytic_id': analytic,
                'lot_serial': line.lot_serial,
                'is_select': True,
            }))
        return line_sale

    def create_invoice(self):
        sale = self.env['sale.order'].browse(self._context.get('active_id'))
        res = False
        if sale.use_invoice_plan:
            res = sale.action_invoice_create_plan()
        else:
            res = super(SaleInvoiceSelect, self).create_invoice()
        return res
