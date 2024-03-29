# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleCreateInvoicePlan(models.TransientModel):
    _name = 'sale.create.invoice.plan'
    _description = 'Fillig invoice planning criteria'

    advance = fields.Boolean(
        string='Advance on 1st Invoice',
        default=False,
    )
    advance_amount = fields.Float(
        string='Advance Amount',
        default=0.0,
    )
    num_installment = fields.Integer(
        string='Number of Installment',
        default=0,
        required=True,
    )
    installment_date = fields.Date(
        string='Installment Date',
        default=fields.Date.context_today,
        required=True,
    )
    interval = fields.Integer(
        string='Interval',
        default=1,
        required=True,
    )
    interval_type = fields.Selection(
        [('day', 'Day'),
         ('month', 'Month'),
         ('year', 'Year')],
        string='Interval Type',
        default='month',
        required=True,
    )

    @api.one
    @api.constrains('num_installment')
    def _check_num_installment(self):
        if self.num_installment <= 0:
            raise ValidationError(_('Number Installment must greater than 0'))

    @api.multi
    def sale_create_invoice_plan(self):
        sale = self.env['sale.order'].browse(self._context.get('active_id'))
        self.ensure_one()
        sale.create_invoice_plan(self.num_installment,
                                 self.installment_date,
                                 self.interval,
                                 self.interval_type,
                                 self.advance,
                                 self.advance_amount)
        return {'type': 'ir.actions.act_window_close'}
