# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, exceptions

class Project(models.Model):

    _inherit = 'project.project'
    _description = 'Project'

    def _compute_partner_claim(self):
        for obj in self:
            claim_data = obj.env['crm.claim'].read_group(
                domain=[('partner_id', 'child_of', [obj.partner_id.id])],
                fields=['partner_id'],
                groupby=['partner_id']
            )
            if claim_data:
                obj.partner_claim = claim_data[0]['partner_id_count']

    partner_claim = fields.Integer(
        'Number of claim from the same partner',
        compute='_compute_partner_claim'
    )

    project_list_ids = fields.One2many(
        "project.project.line",
        "project_id",
        string="Technician List",
        required=False,
    )

    project_estimate_ids = fields.One2many(
        "project.project.estimate",
        "project_id",
        string="Project Estimate Budget",
        required=False,
    )

    stock_request_ids = fields.One2many(
        "stock.request",
        "project_id",
        string="Stock Request",
        required=False,
    )

    service_ids = fields.One2many(
        "sale.service",
        "project_id",
        string="Contract",
        required=False,
    )

    helpdesk_ids = fields.One2many(
        "crm.helpdesk",
        "project_id",
        string="Job",
        required=False,
    )

    project_sale_ids = fields.One2many(
        comodel_name='project.sale',
        inverse_name='project_id',
        string='Sale Job',
    )

    sale_ids = fields.One2many(
        comodel_name='sale.order',
        inverse_name='project_sale_id',
        string='Sale',
        help='Help note'
    )

    amount_total = fields.Float(
        compute="_compute_amount",
        string="Amount",
        track_visibility='onchange',
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('reject', 'Reject'),
        ],
        string='State',
        default='draft',
    )

    @api.multi
    def open_partner_claim(self):
        for obj in self:
            return {
                'type': 'ir.actions.act_window',
                'name': _('Claims'),
                'res_model': 'crm.claim',
                'view_mode': 'tree,form',
                'context': {'search_default_partner_id': self.partner_id.id}
            }

    @api.multi
    def _compute_amount(self):
        for Estimate in self:
            Estimate.amount_total = sum(line.amount for line in Estimate.project_estimate_ids)

    @api.model
    def create(self, vals):
        if 'name' in vals and vals.get('name'):
            if self.search([('name', '=', vals.get('name'))]):
                raise exceptions.Warning(
                    _('Cannot create existing project.'))
        return super(Project, self).create(vals)

class ProjectLine(models.Model):

    _name = 'project.project.line'
    _description = 'Project line'

    partner_id = fields.Many2one(
        "res.partner",
        string="Project Team",
        required=False,
        domain="[('service', '=', True)]",
    )

    users_id = fields.Many2one(
        "res.users",
        string="Project Team",
        required=False,
    )

    position = fields.Selection([
            ('pa', 'PA'),
            ('ra', 'RA'),
            ('steward', 'Steward'),
            ('laundry', 'Laundry'),
        ],
        string="Position"
    )
    description = fields.Char(
        'Description',
    )
    time_period = fields.Char(
        'Time Period',
    )
    start_date = fields.Date(
        'Start Date',
    )
    finish_date = fields.Date(
        'Finish Date',
    )
    date_time_working = fields.Char(
        'Date-time Working',
    )

    project_id = fields.Many2one(
        "project.project",
        string="Project",
        required=False,
    )

class ProjectEstimate(models.Model):

    _name = 'project.project.estimate'
    _description = 'Project Estimate'

    product_id = fields.Many2one(
        "product.product",
        string="Product",
        required=False,
    )

    qty = fields.Float(
        string="Qty",
        required=False,
        default=0,
    )

    uom_id = fields.Many2one(
        "product.uom",
        string="UOM",
        required=False,
    )

    amount = fields.Float(
        string="Amount",
        required=False,
        default=0,
    )

    project_id = fields.Many2one(
        "project.project",
        string="Project",
        required=False,
    )

class ProjectSale(models.Model):
    _name = 'project.sale'
    _description = 'Sale of Project'

    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Project',
    )
    sale_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sale',
    )
    start_date = fields.Date(
        string='Start Date',
    )
    end_date = fields.Date(
        string='End Date',
    )
    department = fields.Selection([
            ('om', 'OM'),
            ('hc', 'HC'),
            ('bc', 'BC'),
        ],
        string="หน่วยงาน",
        related='sale_id.department',
    )
    job_category = fields.Selection([
        ('pa', 'Public Area'),
        ('ra', 'Room Attendance'),
        ('st', 'Steward'),
        ('la', 'Laundry'),
        ('el', 'Electrician'),
        ('ca', 'carpenter'),
        ('ga', 'Gardener'),
        ('ma', 'Mason'),
        ('ba', 'Bakery Staff'),
        ('hm', 'Houseman'),
        ('pt', 'Painter'),
    ],
    string="ประเภทการทำความสะอาด")
    number_maid = fields.Integer(
        string='Number of Maid',
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('reject', 'Reject'),
        ],
        string='State',
        default='draft',
    )

