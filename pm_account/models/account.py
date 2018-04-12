from odoo import api, fields, models, _, exceptions

class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    contract_no = fields.Char(
        'Contract NO.',
    )

class AccountVoucher(models.Model):
    _inherit = 'account.voucher'

    parent_invoice_id = fields.Many2one(
        'account.invoice',
        'Parent'
    )


class AccountAccuredIncome(models.Model):
    _name = 'account.accured.income'

    date_trans = fields.Date(
        'Transaction Date'
    )
    date_entry = fields.Date(
        'Entry Date'
    )
    journal_id = fields.Many2one(
        'account.journal',
        'Journal',
        readonly=False,
    )
    account_id = fields.Many2one(
        'account.account',
        'Account'
    )
    accured_line_ids = fields.One2many(
        'account.accured.income.line',
        'accured_id',
        'Accured Line'
    )


class AccountAccuredIncomeLine(models.Model):
    _name = 'account.accured.income.line'

    accured_id = fields.Many2one(
        'account.accured.income',
        'Accured'
    )
    invoice_id = fields.Many2one(
        'account.invoice',
        'Invoice No.'
    )
    partner_id = fields.Many2one(
        'res.partner',
        'Partner'
    )
    total_amount = fields.Float(
        'Total Amount'
    )
    amount_last_month = fields.Float(
        'Amount Last Month'
    )
    amount = fields.Float(
        'Amount'
    )
