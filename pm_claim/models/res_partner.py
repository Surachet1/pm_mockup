# -*- coding: utf-8 -*-
from openerp import api, fields, models, _

class Partner(models.Model):
    _inherit = "res.partner"

    def _compute_partner_claim(self):
        for obj in self:
            claim_data = obj.env['crm.claim'].read_group(
                domain=[('partner_id', 'child_of', obj.ids)],
                fields=['partner_id'],
                groupby=['partner_id']
            )
            if claim_data:
                obj.partner_claim = claim_data[0]['partner_id_count']

    partner_claim = fields.Integer(
        'Number of claim from the same partner',
        compute='_compute_partner_claim'
    )

    @api.multi
    def open_partner_claim(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Claims'),
            'res_model': 'crm.claim',
            'view_mode': 'tree,form',
            'context': {'search_default_partner_id': self.id}
        }
