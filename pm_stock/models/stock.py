# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, exceptions

class Picking(models.Model):

    _inherit = 'stock.picking'

    remind_ids = fields.One2many(
        comodel_name='stock.remind',
        inverse_name='picking_id',
        string='Remind',
    )


class PickingRemind(models.Model):

    _name = 'stock.remind'

    picking_id = fields.Many2one(
        comodel_name='stock.picking',
        string='Picking',
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
    )
    lot_serial = fields.Char(
        string='Lot/Serial No.',
        size=64,
    )
    description = fields.Char(
        string='Description',
        size=64,
    )
    date_remind = fields.Datetime(
        string='Date Remind',
    )
    date_expired = fields.Datetime(
        string='Expired Date',
    )
