# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, exceptions
import time

class CRMClaim(models.Model):
    _name = "crm.claim"
    _inherit = ['mail.thread']

    name = fields.Char(
        'Claim Subject',
        required=True
    )
    active = fields.Boolean(
        'Active',
        default=True
    )
    action_next = fields.Char(
        'Next Action'
    )
    date_action_next = fields.Datetime(
        'Next Action Date'
    )
    description = fields.Text(
        'Description'
    )
    resolution = fields.Text(
        'Resolution'
    )
    create_date = fields.Datetime(
        'Creation Date',
        readonly=True
    )
    write_date = fields.Datetime(
        'Update Date',
        readonly=True
    )
    state = fields.Selection([
            ('draft', 'Draft'),
            ('in_progress', 'In Progress'),
            ('complete', 'Completed'),
            ('incomplete', 'Incompleted'),
        ],
        string="State"
    )
    depart_respond = fields.Selection([
            ('hc', 'HC'),
            ('oms', 'OMS'),
            ('omm', 'OMM'),
            ('oml', 'OML'),
        ],
        string="หน่วยงานรับผิดชอบ"
    )
    date_deadline = fields.Date(
        'Deadline'
    )
    date_closed = fields.Datetime(
        'Closed',
        readonly=True
    )
    date = fields.Datetime(
        'Claim Date',
        select=True
    )
    priority = fields.Selection([
            ('0','Low'),
            ('1','Normal'),
            ('2','High'),
            ('3','Urgent')
        ],
        'Priority'
    )
    type_action = fields.Selection([
            ('correction','Corrective Action'),
            ('prevention','Preventive Action')
        ],
        'Action Type'
    )
    user_id = fields.Many2one(
        'res.users',
        'Responsible',
        track_visibility='always'
    )
    user_fault = fields.Char(
        'Trouble Responsible'
    )
    team_id = fields.Many2one(
        'crm.team',
        'Sales Team',
    )
    company_id = fields.Many2one(
        'res.company',
        'Company'
    )
    partner_id = fields.Many2one(
        'res.partner',
        'Partner',
        domain="[('customer', '=', True),('parent_id', '=', False)]"
    )
    email_from = fields.Char(
        'Email',
        size=128,
        help="Destination email for email gateway."
    )
    partner_phone = fields.Char(
        'Phone'
    )
    cause = fields.Text(
        'Root Cause'
    )
    categ_res_type_id = fields.Many2one(
        'respond.type',
        string="Category",
        domain="[('parent_id','=',False)]"
    )
    title_res_type_id = fields.Many2one(
        'respond.type',
        string="Title",
        domain="[('parent_id','=',categ_res_type_id)]"
    )
    list_res_type_id = fields.Many2one(
        'respond.type',
        string="List",
        domain="[('parent_id','=',title_res_type_id)]"
    )
    cost_defect = fields.Char(
        'มูลลค่าความเสียหาย'
    )
    recommend = fields.Char(
        'ข้อเสนอแนะ'
    )
    feedback = fields.Char(
        'Feedback'
    )


class RespondType(models.Model):
    _name = 'respond.type'
    _description = 'Respond Type'

    name = fields.Char(
        required=True,
        translate=True
    )
    parent_id = fields.Many2one(
        'respond.type',
        'Parent Type',
        domain="[('id','!=',active_id)]"
    )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', _("Type name already exists !")),
    ]
