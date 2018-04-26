# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil import relativedelta
from odoo import api, fields, models, _, exceptions
import openerp.addons.decimal_precision as dp
from odoo.exceptions import UserError, AccessError, ValidationError

class Service(models.Model):
    _name = 'sale.service'
    _inherit = ['mail.thread']

    @api.multi
    def _month_count(self):
        for line in self:
            date_format = '%Y-%m-%d'
            d1 = datetime.strptime(line.start_date, date_format).date()
            d2 = datetime.strptime(line.finish_date, date_format).date()
            line.month_count = (d2.year - d1.year)*12 + d2.month - d1.month

    name = fields.Char(
        'Service NO',
        size=24,
        readonly=True
    )
    type = fields.Selection([
            ('om', 'OM'),
            ('hc', 'HC'),
        ],
        string="Type"
    )
    start_date = fields.Date(
        'Start Date',
        required=True
    )
    finish_date = fields.Date(
        'Finish Date',
        required=True
    )
    serial_no = fields.Many2many(
        'stock.production.lot',
        'sale_service_serial_no_rel',
        'service_id',
        'serial_id',
        string='Serial NO.'
    )
    sale_order = fields.Many2one(
        'sale.order',
        string='Sale Order',
        required=True,
    )
    service_count = fields.Integer(
        'Service Available',
        readonly=True
    )
    service_count_show = fields.Integer(
        string='Service Available',
        related='service_count',
        readonly=True,
    )
    service_amount = fields.Integer(
        'Service Amount',
        required=True,
    )
    detail = fields.Text(
        'Detail',
        size=400
    )
    state = fields.Selection([
            ('draft','Draft'),
            ('active','Active'),
            ('expiring','Expiring'),
            ('expired','Expired'),
            ('terminate','Terminated')
        ],
        'Status',
        readonly=True,
        track_visibility='onchange',
        help="Gives the status of the services ",
        select=True,
        default='draft',
    )
    customer = fields.Many2one(
        'res.partner',
        string="Customer",
        track_visibility='always',
    )
    project_id = fields.Many2one(
        'project.project',
        'Project'
    )
    month_count = fields.Integer(
        compute="_month_count",
        string='Month Available',
        track_visibility='always',
    )
    phone = fields.Char(
        related='customer.phone',
        string="Phone",
        readonly=True,
        track_visibility='always',
    )
   #sale_order_date = fields.related(
   #    'sale_order',
   #    'date_order',
   #    type="char",
   #    string="Sale Order Date",
   #    readonly=True
   #)
    sale_order_date = fields.Datetime(
        string="Sale Order Date",
        related='sale_order.date_order',
        readonly=True,
    )
    service_list =fields.Many2many(
        'crm.helpdesk',
        'crm_service_rel',
        'service_id',
        'crm_id',
        string="Service Contract",
        readonly=True,
    )
    job_count = fields.Integer(
        string='Job Count',
        compute='_calculate_job_count',
        store=True,
        readonly=True,
    )

    contract_no = fields.Char(
        string='Contract NO',
        #related='sale_order.contract_no',
        readonly=True,
    )
    invoice_no = fields.Char(
        string='Invoice NO',
        readonly=True,
        #related='sale_order.invoice_no',
    )
    receipt_no = fields.Char(
        string='Receipt NO',
        readonly=True,
        #related='sale_order.receipt_no',
    )
    ref_service_id = fields.Many2one(
        'sale.service',
        string='Ref. Service Contract',
        readonly=True,
    )
    extend_count = fields.Integer(
        string='Extension Count',
        readonly=True,
    )
    package_price = fields.Float(
        string='Service Price/Time',
        required=True,
        digits_compute=dp.get_precision('Product Price'),
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    customer_code = fields.Char(
        string="Code",
        #related='customer.x_id_customer',
        store=True,
        readonly=True,
    )
    customer_address = fields.Char(
        string="Address",
        compute="get_customer_address",
        readonly=True,
    )
    detail = fields.Text(
        states={
            'draft': [('readonly', False)],
            'active': [('readonly', False)],
            'expiring': [('readonly', False)],
        },
    )
    sale_comment = fields.Text(
        string='Sale Comment',
    )

    def button_active(self):
        for obj in self:
            obj.write({"state": "active"})
        return True

    def button_terminate(self):
        for obj in self:
            obj.write({"state": "terminate"})
        return True

    @api.depends('service_list')
    @api.multi
    def _calculate_job_count(self):
        for service in self:
            service.job_count = len(service.service_list)

    @api.depends('customer')
    def get_customer_address(self):
        for service in self:
            display_text = "%s %s \n %s %s" % (
                service.customer.street or '',
                service.customer.street2 or '',
                service.customer.city or '',
                service.customer.zip or '',
            )
            if service.customer.street:
                service.customer_address = \
                    "%s" % (display_text[:60])
