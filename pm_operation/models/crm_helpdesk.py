# -*- coding: utf-8 -*-

import openerp
#from openerp.addons.crm import crm
#from openerp.osv import fields, osv
from odoo import api, fields, models, _, exceptions
from openerp import tools
from openerp.tools.translate import _
from openerp.tools import html2plaintext
from datetime import datetime
from odoo.exceptions import UserError, ValidationError

class crm_helpdesk(models.Model):
    """ Helpdesk Cases """

    _name = "crm.helpdesk"
    _description = "Helpdesk"
    _order = "id desc"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    id = fields.Integer(
        'ID',
        readonly=True
    )
    type = fields.Selection([
            ('om', 'OM'),
            ('hc', 'HC'),
        ],
        string="Type"
    )
    name = fields.Char(
        'Name',
        required=True
    )
    active = fields.Boolean(
        'Active',
        required=False,
        default=True
    )
    date_action_last = fields.Datetime(
        'Last Action',
        readonly=1
    )
    date_action_next = fields.Datetime(
        'Next Action',
        readonly=1
    )
    description = fields.Text(
        'Description'
    )
    create_date = fields.Datetime(
        'Creation Date' ,
        readonly=True
    )
    write_date = fields.Datetime(
        'Update Date' ,
        readonly=True
    )
    date_deadline = fields.Date(
        'Deadline'
    )
    user_id = fields.Many2one(
        'res.users',
        'Responsible'
    )
    project_id = fields.Many2one(
        'project.project',
        'Project'
    )
    #section_id
    team_id = fields.Many2one(
        'crm.team',
        'Sales Team'
    )
    company_id = fields.Many2one(
        'res.company',
        'Company'
    )
    date_closed = fields.Datetime(
        'Closed',
        readonly=True
    )
    partner_id = fields.Many2one(
        'res.partner',
        'Partner'
    )
    email_cc = fields.Text(
        'Watchers Emails',
        size=252
    )
    email_from = fields.Char(
        'Email',
        size=128,
        help="Destination email for email gateway"
    )
    date = fields.Datetime(
        'Date'
    )
   #ref = fields.Reference(
   #    'Reference',
   #    selection=openerp.addons.base.res.res_request.referencable_models
   #)
   #ref2 = fields.Reference(
   #    'Reference 2',
   #    selection=openerp.addons.base.res.res_request.referencable_models
   #)
   #channel_id = fields.Many2one(
   #    'crm.tracking.medium',
   #    'Channel',
   #    help="Communication channel."
   #)
    planned_revenue = fields.Float(
        'Planned Revenue'
    )
    planned_cost = fields.Float(
        'Planned Costs'
    )
    priority = fields.Selection([
            ('0','Low'),
            ('1','Normal'),
            ('2','High')
        ],
        'Priority'
    )
    probability = fields.Float(
        'Probability (%)'
    )
   #categ_id = fields.Many2one(
   #    'crm.case.categ',
   #    'Category',
   #    domain="['|',
   #    ('section_id','=',False),
   #    ('section_id','=',section_id),
   #    ('object_id.model','=','crm.helpdesk')]"
   #)
    duration = fields.Float(
        'Duration'
    )
    state = fields.Selection([
            ('draft', 'New'),
            ('open', 'In Progress'),
            ('pending', 'Pending'),
            ('done', 'completed'),
            ('cancel', 'Cancelled')
        ],
        'Status',
        readonly=True,
        track_visibility='onchange',
        default='done',
    )
    seq = fields.Char(
        'After Sale NO.',
        size=24,
        readonly=True
    )
    detail = fields.Text(
        'Order detail',
        size=400
    )
    problem = fields.Text(
        'Problem',
        size=400
    )
    record = fields.Text(
        'Memo',
        size=400
    )
    customer_review = fields.Text(
        'Customer Comment',
        size=400
    )
    service_type = fields.Selection([
            ('new','New (1 service count)'),
            ('re-open','Re-open (no service count)'),
            ('incomplete','Incomplete (no service count)'),
            ('repair','Repair (no service count)')
        ],
        'Service type'
    )
    customer_score = fields.Selection([
            (5,'5'),
            (4,'4'),
            (3,'3'),
            (2,'2'),
            (1,'1')
        ],
        'Customer Score',
        type='integer'
    )
    overseer_score = fields.Selection([
            (5,'5'),
            (4,'4'),
            (3,'3'),
            (2,'2'),
            (1,'1')
        ],
        'Overseer Score',
        type='integer'
    )
    users_response = fields.Many2many(
        'res.partner',
        'res_partner_crm_rel',
        'partner_id',
        'crm_id',
        string='Responsible'
    )
    service_head = fields.Many2one(
        'res.partner',
        'Service team',
    )
    service = fields.Many2many(
        'res.partner',
        'crm_helpdesk_service_rel',
        'helpdesk_id',
        'partner_id',
        string='Service Persons'
    )
    service_order = fields.Many2many(
        'sale.service',
        'crm_service_rel',
        'crm_id',
        'service_id',
        string='Services'
    )
    phone = fields.Char(
        related='partner_id.phone',
        string="Phone",
        readonly=False,
        track_visibility='always',
    )
    is_close = fields.Boolean(
        'Is Close'
    )
    street = fields.Char(
        string='Street',
        size=128,
    )
    date_display = fields.Datetime(
        string='Date Display',
        related='date',
    )
    date_cal = fields.Date(
        string='Select Date',
        required=True,
        #readonly=True,
        states={'draft': [('readonly', False)]},
    )
    select_day_cal = fields.Selection(
        [
            ('morning', 'Morning'),
            ('afternoon', 'Afternoon'),
        ],
        string='Select Time Range',
        required=True,
        #readonly=True,
        states={'draft': [('readonly', False)]},
    )
    hour_cal = fields.Integer(
        string='Hour(s)',
        required=True,
        #readonly=True,
        states={'draft': [('readonly', False)]},
    )
    minute_cal = fields.Integer(
        string='Minute(s)',
        required=True,
        #readonly=True,
        states={'draft': [('readonly', False)]},
    )
    customer_code = fields.Char(
        string="Code",
        #compute="get_customer_detail",
        store=True,
        readonly=False,
    )
    customer_address = fields.Char(
        string="Address",
        #compute="get_customer_detail",
        readonly=True,
    )
    customer_address_display = fields.Char(
        string="Address",
        #compute="set_address_display",
        readonly=True,
    )
    service_type2 = fields.Many2one(
        'sale.service.type',
        'Service Type',
        #readonly=True,
        states={'draft': [('readonly', False)]},
        ondelete='restrict',
    )
    emp_ids = fields.Many2many(
        comodel_name='hr.employee',
        string='Employee',
    )
