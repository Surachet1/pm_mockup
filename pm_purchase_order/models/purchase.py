# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, exceptions

class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    description = fields.Text('Notes')

    date_start = fields.Date('Start Date')
    date_end = fields.Date('End Date')
