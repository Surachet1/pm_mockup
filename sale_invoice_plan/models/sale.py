# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_compare, float_round as round,float_is_zero


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    @api.depends('invoice_lines.invoice_id.state', 'invoice_lines.quantity')
    def _get_invoice_qty(self):
        """
        Compute the quantity invoiced. If case of a refund, the quantity invoiced is decreased. Note
        that this is the case only if the refund is generated from the SO and that is intentional: if
        a refund made would automatically decrease the invoiced quantity, then there is a risk of reinvoicing
        it automatically, which may not be wanted at all. That's why the refund has to be created from the SO
        """
        for line in self:
            qty_invoiced = 0.0
            for invoice_line in line.invoice_lines:
                if invoice_line.invoice_id.state != 'cancel':
                    if invoice_line.invoice_id.type == 'out_invoice':
                        qty_invoiced += invoice_line.uom_id._compute_quantity(invoice_line.quantity, line.product_uom)
                    elif invoice_line.invoice_id.type == 'out_refund':
                        qty_invoiced -= invoice_line.uom_id._compute_quantity(invoice_line.quantity, line.product_uom)
            line.qty_invoiced = qty_invoiced
            if line.order_id.use_invoice_plan:
                line.qty_invoiced = line.qty_delivered

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    invoice_plan_ids = fields.One2many(
        comodel_name='sale.invoice.plan',
        inverse_name='sale_id',
        string='Inovice Plan',
        copy=False,
    )
    invoice_complete = fields.Boolean(
        string="Invoiced complete",
        compute='_compute_invoice_complete'
    )
    use_invoice_plan = fields.Boolean(
        string='Use Invoice Plan',
        default=False,
        copy=False,
    )
    ip_invoice_plan = fields.Boolean(
        string='Invoice Plan In Process',
        compute='_compute_ip_invoice_plan',
        help="At least one invoice plan line pending to create invoice",
    )

    @api.multi
    def _compute_invoice_complete(self):
        for rec in self:
            res = True
            for ip in rec.invoice_plan_ids:
                if not ip.invoiced:
                    res = False
                    break
            if not rec.use_invoice_plan:
                res = False
        rec.invoice_complete = res

    @api.multi
    def _compute_ip_invoice_plan(self):
        for rec in self:
            rec.ip_invoice_plan = rec.use_invoice_plan and \
                rec.invoice_plan_ids and \
                len(rec.invoice_plan_ids.filtered(lambda l: not l.invoiced))

    @api.constrains('state')
    def _check_invoice_plan(self):
        for rec in self:
            if rec.state != 'draft':
                if rec.invoice_plan_ids.filtered(lambda l: not l.percent):
                    raise ValidationError(
                        _('Please fill percentage for all invoice plan lines'))

    @api.multi
    def action_confirm(self):
        if self.filtered(lambda r: r.use_invoice_plan
                         and not r.invoice_plan_ids):
            raise UserError(
                _('Use Invoice Plan selected, but no plan created'))
        return  super(SaleOrder, self).action_confirm()
        #  super().action_confirm()

    @api.multi
    def create_invoice_plan(self, num_installment, installment_date,
                            interval, interval_type, advance,advance_amount):
        self.ensure_one()
        self.invoice_plan_ids.unlink()
        invoice_plans = []
        Decimal = self.env['decimal.precision']
        prec = Decimal.precision_get('Percent')
        # percent = round(1.0 / num_installment * 100, prec)
        # percent_last = 100 - (percent * (num_installment-1))
        # amount = round(self.amount_untaxed * percent,2)/100
        # amount_last = round(self.amount_untaxed * percent_last,2)/100
        advance_percent = percent = percent_last = 0.0
        amount = amount_last = balance_amount = 0.0
        # Advance
        if not advance:
            advance_amount = 0.0
        balance_amount = self.amount_after_discount - advance_amount
        advance_percent = (advance_amount/self.amount_after_discount)*100
        percent = round(1.0 / num_installment * (100-advance_percent), prec)
        amount = round(self.amount_after_discount * percent, 2) / 100
        percent_last = (100-advance_percent) - (percent * (num_installment - 1))
        amount_last = round(self.amount_after_discount * percent_last, 2) / 100
        if advance:
            vals = {'installment': 0, 'plan_date': installment_date,
                    'invoice_type': 'advance', 'percent': advance_percent,'amount':advance_amount,'invoiced':True}
            invoice_plans.append((0, 0, vals))
            installment_date = self._next_date(installment_date,
                                               interval, interval_type)

        # Normal
        # percent = round(1.0 / num_installment * 100, prec)
        # percent_last = 100 - (percent * (num_installment - 1))
        # amount = round(self.amount_untaxed * percent, 2) / 100
        # amount_last = round(self.amount_untaxed * percent_last, 2) / 100
        amount = balance_amount/num_installment
        percent = (amount/self.amount_after_discount)*100
        percent_last = (100-advance_percent) - (percent * (num_installment - 1))
        amount_last = round(balance_amount * percent_last, 2) / 100
        for i in range(num_installment):
            this_installment = i+1
            if num_installment == this_installment:
                percent = percent_last
                # amount = amount_last
            vals = {'installment': this_installment,
                    'plan_date': installment_date,
                    'invoice_type': 'installment',
                    'percent': percent,
                    'amount':amount}
            invoice_plans.append((0, 0, vals))
            installment_date = self._next_date(installment_date,
                                               interval, interval_type)
        self.write({'invoice_plan_ids': invoice_plans})
        return True

    @api.multi
    def remove_invoice_plan(self):
        self.ensure_one()
        self.invoice_plan_ids.unlink()
        return True

    @api.model
    def _next_date(self, installment_date, interval, interval_type):
        installment_date = fields.Date.from_string(installment_date)
        if interval_type == 'month':
            next_date = installment_date + relativedelta(months=+interval)
        elif interval_type == 'year':
            next_date = installment_date + relativedelta(years=+interval)
        else:
            next_date = installment_date + relativedelta(days=+interval)
        next_date = fields.Date.to_string(next_date)
        return next_date

    @api.multi
    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        order_type = self.order_line.mapped('order_type')
        if ('project') in order_type:
            res['main_order_type'] = 'project'
        elif ('refurbished') in order_type or ('new') in order_type or ('license') in order_type:
            res['main_order_type'] = 'product'
        else:
            res['main_order_type'] = 'service'
        return res

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        """
        Create the invoice associated to the SO.
        :param grouped: if True, invoices are grouped by SO id. If False, invoices are grouped by
                        (partner_invoice_id, currency)
        :param final: if True, refunds will be generated if necessary
        :returns: list of created invoices
        """
        inv_obj = self.env['account.invoice']
        precision = self.env['decimal.precision'].precision_get('Percent')
        invoices = {}
        references = {}
        invoices_origin = {}
        invoices_name = {}
        for order in self:
            group_key = order.id if grouped else (order.partner_invoice_id.id, order.currency_id.id)
            for line in order.order_line.sorted(key=lambda l: l.qty_delivered < 0):
                if float_is_zero(line.qty_delivered, precision_digits=precision):
                    continue
                if group_key not in invoices:
                    inv_data = order._prepare_invoice()
                    invoice = inv_obj.create(inv_data)
                    references[invoice] = order
                    invoices[group_key] = invoice
                    invoices_origin[group_key] = [invoice.origin]
                    invoices_name[group_key] = [invoice.name]
                elif group_key in invoices:
                    if order.name not in invoices_origin[group_key]:
                        invoices_origin[group_key].append(order.name)
                    if order.client_order_ref and order.client_order_ref not in invoices_name[group_key]:
                        invoices_name[group_key].append(order.client_order_ref)

#                 if line.qty_to_invoice > 0:
                line.invoice_line_create(invoices[group_key].id, line.qty_delivered)
#                 elif line.qty_to_invoice < 0 and final:
#                     line.invoice_line_create(invoices[group_key].id, line.qty_to_invoice)

            if references.get(invoices.get(group_key)):
                if order not in references[invoices[group_key]]:
                    references[invoice] = references[invoice] | order

        for group_key in invoices:
            invoices[group_key].write({'name': ', '.join(invoices_name[group_key]),
                                       'origin': ', '.join(invoices_origin[group_key])})

        if not invoices:
            raise UserError(_('There is no invoicable line.'))

        for invoice in invoices.values():
            invoice.compute_taxes()
            if not invoice.invoice_line_ids:
                raise UserError(_('There is no invoicable line.'))
            # If invoice is negative, do a refund invoice instead
            if invoice.amount_total < 0:
                invoice.type = 'out_refund'
                for line in invoice.invoice_line_ids:
                    line.quantity = -line.quantity
            # Use additional field helper function (for account extensions)
            for line in invoice.invoice_line_ids:
                line._set_additional_fields(invoice)
            # Necessary to force computation of taxes. In account_invoice, they are triggered
            # by onchanges, which are not triggered when doing a create.
            invoice.compute_taxes()
            invoice.message_post_with_view('mail.message_origin_link',
                values={'self': invoice, 'origin': references[invoice]},
                subtype_id=self.env.ref('mail.mt_note').id)
        return [inv.id for inv in invoices.values()]

    @api.multi
    def action_invoice_create_plan(self, grouped=False, final=False):
        inv_ids = False
        ip_obj = False
        for ip in self.invoice_plan_ids:
            if ip.to_invoice:
                ip_obj = ip
                break
        # invoice_plan_id = False
        # if ip_obj:
        #     invoice_plan_id = ip_obj.id
        if ip_obj:
            plan = ip_obj
            if plan.invoice_type != 'advance':
                inv_ids = self.action_invoice_create(grouped=grouped, final=final)
            plan.invoiced = True
            plan.to_invoice = False
            next_plan = False
            for ip in self.invoice_plan_ids:
                if ip.installment==plan.installment+1:
                    next_plan=ip
            if next_plan:
                next_plan.to_invoice = True
            invoices = self.env['account.invoice'].browse(inv_ids)
            invoices.ensure_one()  # Expect 1 invoice for 1 invoice plan
            plan._compute_new_invoice_quantity(invoices[0])
            invoices[0].date_invoice = plan.plan_date
            plan.invoice_ids += invoices
        return inv_ids

    @api.multi
    def cal_invoice_plan(self):
        for rec in self:
            inv_plan = self.env['sale.invoice.plan']
            amount_after_discount = self.amount_after_discount
            number = 0
            amt_invoiced = 0
            for pl_line in rec.invoice_plan_ids:
                if pl_line.to_invoice or pl_line.invoiced:
                    amt_invoiced += pl_line.amount
                else:
                    inv_plan += pl_line
                    number += 1
            if amt_invoiced > 0:
                amt_remain = amount_after_discount - amt_invoiced
                if amt_remain > 0 and number > 0:
                    amt_period = amt_remain / number
                    percent = (amt_period / amount_after_discount) * 100
                    for pl in inv_plan:
                        pl.write({
                            'amount': amt_period,
                            'percent': percent,
                        })



class SaleInvoicePlan(models.Model):
    _name = 'sale.invoice.plan'
    _description = 'Invoice Planning Detail'
    _order = 'installment'

    sale_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sales Order',
        index=True,
        readonly=True,
        ondelete='cascade',
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        related='sale_id.partner_id',
        store=True,
        index=True,
    )
    state = fields.Selection(
        [('draft', 'Quotation'),
         ('sent', 'Quotation Sent'),
         ('sale', 'Sales Order'),
         ('done', 'Locked'),
         ('cancel', 'Cancelled'), ],
        string='Status',
        related='sale_id.state',
        store=True,
        index=True,
    )
    installment = fields.Integer(
        string='Installment',
    )
    plan_date = fields.Date(
        string='Plan Date',
        required=True,
    )
    invoice_type = fields.Selection(
        [('advance', 'Advance'),
         ('normal', 'Normal'),
         ('installment', 'Installment'), ],
        string='Type',
        required=True,
        default='installment',
    )
    last = fields.Boolean(
        string='Last Installment',
        compute='_compute_last',
        help="Last installment will create invoice use remaining amount",
    )
    percent = fields.Float(
        string='Percent',
        digits=dp.get_precision('Percent'),
        help="This percent will be used to calculate new quantity"
    )
    amount = fields.Float(
        string='Amount installment',
    )
    invoice_ids = fields.Many2many(
        'account.invoice',
        relation="sale_invoice_plan_invoice_rel",
        column1='plan_id', column2='invoice_id',
        string='Invoices',
        readonly=True,
    )
    to_invoice = fields.Boolean(
        string='Next Invoice',
        # compute='_compute_to_invoice',
        help="If this line is ready to create new invoice",
    )
    invoiced = fields.Boolean(
        string='Invoice Created',
        # compute='_compute_invoiced',
        help="If this line already invoiced",
    )
    _sql_constraint = [('unique_instalment',
                        'UNIQUE (sale_id, installment)',
                        'Installment must be unique on invoice plan')]

    # @api.onchange('to_invoice')
    # def _compute_to_invoice(self):
    #     """ If any invoice is in draft/open/paid do not allow to create inv
    #         Only if previous to_invoice is False, it is eligible to_invoice
    #     """
        # for rec in self.sorted('installment'):
        #     rec.to_invoice = False
        #     if rec.sale_id.state != 'sale':  # Not confirmed, no to_invoice
        #         continue
        #     if not rec.invoiced:
        #         rec.to_invoice = True
        #         break

    # @api.onchange('invoiced')
    # def _compute_invoiced(self):
    #     for rec in self:
    #         invoiced = rec.invoice_ids.filtered(
    #             lambda l: l.state in ('draft', 'open', 'paid'))
    #         rec.invoiced = invoiced and True or False

    @api.onchange('amount')
    def _onchange_amount(self):
        for rec in self:
            amount_after_discount = rec.sale_id.amount_after_discount
            if rec.amount > 0 and amount_after_discount > 0:
                percent = (rec.amount / amount_after_discount) * 100
                rec.percent = percent

    @api.multi
    def _compute_last(self):
        for rec in self:
            last = max(rec.sale_id.invoice_plan_ids.mapped('installment'))
            rec.last = rec.installment == last

    @api.multi
    def _compute_new_invoice_quantity(self, invoice):
        self.ensure_one()
        # if self.last:  # For last install, let the system do the calc.
        #     return
        percent = self.percent
        for line in invoice.invoice_line_ids:
            assert len(line.sale_line_ids) >= 0, \
                'No matched order line for invoice line'
            order_line = fields.first(line.sale_line_ids)
            if order_line.is_down_payment:
                line.write({'quantity': -percent/100})  # based on 1 unit
            else:
#                 plan_qty = order_line.product_uom_qty * (percent/100)
                # prec = order_line.product_uom.rounding
#                 prec = 0.0001
#                 if float_compare(plan_qty, line.quantity, prec) == 1:
#                     raise ValidationError(
#                         _('Plan quantity: %s, exceed invoiceable quantity: %s'
#                           '\nProduct should be delivered before invoice') %
#                         (plan_qty, line.quantity))
                plan_unit = order_line.price_unit * (percent/100)
                line.write({'price_unit': plan_unit})
        invoice.compute_taxes()
