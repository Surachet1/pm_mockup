# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def _prepare_invoice_line_from_po_line(self, line):
        res = super(AccountInvoice, self)._prepare_invoice_line_from_po_line(line)
        if not res:
            if line.order_id.use_invoice_plan:
                qty = line.product_qty
                analytic = line.account_analytic_id.id
                taxes = line.taxes_id
                invoice_line_tax_ids = line.order_id.fiscal_position_id.map_tax(taxes)
                invoice_line = self.env['account.invoice.line']
                company = self.env['res.company'].browse(1)
                if line.order_id.currency_id != company.currency_id:
                    plan = self.env['purchase.invoice.plan'].search([('purchase_id', '=', line.order_id.id),('to_invoice', '=', True)])
                    if plan:
                        for pl in plan:
                            if pl.to_invoice:
                                price_unit = line.price_unit * (pl.percent / 100)
                    else:
                        price_unit = line.price_unit
                else:
                    price_unit = line.order_id.currency_id.with_context(date=self.date_invoice).compute(line.price_unit, self.currency_id, round=False)
                res = {
                    'purchase_line_id': line.id,
                    'name': line.order_id.name+': '+line.name,
                    'origin': line.order_id.origin,
                    'uom_id': line.product_uom.id,
                    'product_id': line.product_id.id,
                    'account_id': invoice_line.with_context({'journal_id': self.journal_id.id, 'type': 'in_invoice'})._default_account(),
#                     'price_unit': line.order_id.currency_id.with_context(date=self.date_invoice).compute(line.price_unit, self.currency_id, round=False),
                    'price_unit': price_unit,
                    'quantity': qty,
                    'discount': 0.0,
                    'account_analytic_id': analytic,
                    'analytic_tag_ids': line.analytic_tag_ids.ids,
                    'invoice_line_tax_ids': invoice_line_tax_ids.ids,
                    'adj_val': line.adj_val,
                }
                account = invoice_line.get_invoice_line_account('in_invoice', line.product_id, line.order_id.fiscal_position_id, self.env.user.company_id)
                if account:
                    res['account_id'] = account.id
        return res

