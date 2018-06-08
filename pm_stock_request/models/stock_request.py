# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, exceptions
import time
import openerp.addons.decimal_precision as dp


_STATES = [
    ('draft', 'Draft'),
    ('wait_manager_approve', 'Waiting Manager Approve'),
    ('wait_purchase_approve', 'Waiting Purchase Approve'),
    ('approved', 'Picking Management'),
    ('ready', 'Ready to Delivaery'),
    ('done', 'Done'),
    ('rejected', 'Rejected'),
    ('cancel', 'Cancelled')
]


class StockRequest(models.Model):

    _name = 'stock.request'
    _description = 'Stock Request'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    @api.model
    def _company_get(self):
        company_id = self.env['res.company']._company_default_get(self._name)
        return self.env['res.company'].browse(company_id.id)

    @api.model
    def _get_default_requested_by(self):
        return self.env['res.users'].browse(self.env.uid)

    @api.model
    def _get_default_name(self):
        return self.env['ir.sequence'].get('stock.request')

    @api.model
    def _get_default_warehouse(self):
        warehouse_obj = self.env['stock.warehouse']
        company_id = self.env['res.users'].browse(
            self.env.uid).company_id.id
        warehouse = warehouse_obj.search([('company_id', '=', company_id)],
                                         limit=1)
        return warehouse

    @api.multi
    @api.depends('name', 'origin', 'date_start',
                 'requested_by', 'assigned_to', 'description', 'company_id',
                 'line_ids', 'warehouse_id')
    def _get_is_editable(self):
        if self.state in ('wait_manager_approve','wait_purchase_approve', 'approved', 'rejected'):
            self.is_editable = False
        else:
            self.is_editable = True




   #_track = {
   #    'state': {
   #        'purchase_request.mt_request_to_approve':
   #            lambda self, cr, uid, obj,
   #            ctx=None: obj.state == 'to_approve',
   #        'purchase_request.mt_request_approved':
   #            lambda self, cr, uid, obj,
   #            ctx=None: obj.state == 'approved',
   #        'purchase_request.mt_request_rejected':
   #            lambda self, cr, uid, obj,
   #            ctx=None: obj.state == 'rejected',
   #    },
   #}

    name = fields.Char(
        'Request Reference',
        size=32,
        required=True,
        default='New',
        readonly=True
    )
    origin = fields.Char(
        'Source Document',
        size=32
    )
    date_start = fields.Date(
        'Creation date',
        help="Date when the user initiated therequest.",
        default=lambda *args:
        time.strftime('%Y-%m-%d %H:%M:%S'),
        track_visibility='onchange'
    )
    requested_by = fields.Many2one(
        'res.users',
        'Requested by',
        required=True,
        track_visibility='onchange',
        default=_get_default_requested_by
    )
    assigned_to = fields.Many2one(
        'res.users',
        'Approver',
        track_visibility='onchange'
    )
    description = fields.Text(
        'Description'
    )
    company_id = fields.Many2one(
        'res.company',
        'Company',
        required=True,
        default=_company_get,
        track_visibility='onchange'
    )
    line_ids = fields.One2many(
        'stock.request.line',
        'request_id',
        'Products to Purchase',
        readonly=False,
        track_visibility='onchange'
    )
    warehouse_id = fields.Many2one(
        'stock.warehouse',
       string='Warehouse',
       default=_get_default_warehouse,
       track_visibility='onchange'
    )
    state = fields.Selection(
        selection=_STATES,
        string='Status',
        track_visibility='onchange',
        required=True,
        default='draft'
    )
    customer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        required=False,
        domain=[('customer', '=', True)],
    )
    customer_name = fields.Char(
        'Customer Name',
        size=255,
    )
    customer_phone = fields.Char(
        'Customer Phone',
        size=255,
    )
    customer_location = fields.Char(
        'Customer Location',
        size=255,
    )
    schedule_date = fields.Date(
        'Schedule Date',
        default=lambda *args: time.strftime('%Y-%m-%d %H:%M:%S'),
        track_visibility='onchange',
    )
    delivery_note = fields.Text(
        String='Delivery Note',
        readonly=False,
    )
    sale_order_id = fields.Many2one(
        'sale.order',
        string="Sale Order Reference",
    )
    project_id = fields.Many2one(
        'project.project',
        string="Project",
    )
    is_editable = fields.Boolean(
        string="Is editable",
        compute="_get_is_editable",
        readonly=True
    )
    date_contract_start = fields.Date(
        string="Contract Start Date",
        required=False,
    )
    date_contract_finishes = fields.Date(
        string="Contract Finish Date",
        required=False,
    )
    date_received = fields.Date(
        string="Received Date",
        required=False,
    )
    contract_name = fields.Char(
        'Contract Name',
    )
    contract_period = fields.Char(
        'Contract Period',
    )
    budget = fields.Float(
        'Budget',
    )
    balance = fields.Float(
        'Balance',
    )
    sale_type = fields.Selection([
            ('om', 'OM'),
            ('hc', 'HC'),
            ('bc', 'BC'),
        ],
        string="Sale Type"
    )
    remine_ids = fields.One2many(
        comodel_name="stock.request.remine",
        inverse_name="request_id",
        string="Remind",
        required=False,
    )
    is_sale_more = fields.Boolean(
        string="การขายสินค้าเพิ่มเติม"
    )

    @api.one
    def copy(self, default=None):
        default = dict(default or {})
        default.update({
            'state': 'draft',
            'name': self.env['ir.sequence'].get('stock.request'),
        })
        return super(StockRequest, self).copy(default)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].get('stock.request') or 'New'

        if vals.get('assigned_to'):
            assigned_to = self.env['res.users'].browse(vals.get(
                'assigned_to'))
            vals['message_follower_ids'] = [(4, assigned_to.partner_id.id)]

        if len(vals.get('line_ids')) <= 0:
            raise exceptions.Warning(
                _('Choose one or more products line.'))

        return super(StockRequest, self).create(vals)

    @api.multi
    def button_draft(self):
        self.state = 'draft'
        return True

    @api.multi
    def button_to_approve(self):
        self.state = 'wait_manager_approve'
        return True

    @api.multi
    def button_manager_approved(self):
        self.state = 'wait_purchase_approve'
        self.assigned_to = self._uid
        return True

    @api.multi
    def button_purchase_approved(self):
        self.state = 'approved'
        self.assigned_to = self._uid
        return True

    @api.multi
    def button_rejected(self):
        self.state = 'rejected'
        return True

    @api.multi
    def button_cancel(self):
        self.state = 'cancel'
        return True

class StockRequestLine(models.Model):

    _name = "stock.request.line"
    _description = "Stock Request Line"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    @api.one
    def _get_supplier(self):
        if self.product_id:
            for product_supplier in self.product_id.seller_ids:
                self.supplier_id = product_supplier.name

    @api.multi
    @api.depends('product_id', 'name', 'product_uom_id', 'product_qty',
                 'analytic_account_id', 'date_required')
    def _get_is_editable(self):
        for obj in self:
            if obj.request_id.state in ('wait_manager_approve', 'wait_purchase_approve', 'approved', 'rejected'):
                obj.is_editable = False
            else:
                obj.is_editable = True


    product_id = fields.Many2one(
        'product.product', 'Product',
        domain=[('purchase_ok', '=', True)],
        track_visibility='onchange')
    product_type = fields.Selection([
        ('consu', 'Consumable'),
        ('service', 'Service'),
        ('product', 'Stockable Product')],
        'Product Type',
        related="product_id.type",
    )
    qty_available = fields.Float(
        related="product_id.qty_available",
        string="Qty Onhand",
        required=False,
    )
    name = fields.Text(
        'Description',
        size=256,
        track_visibility='onchange')
    product_uom_id = fields.Many2one(
        'product.uom',
        'Product Unit of Measure',
        track_visibility='onchange')
    product_qty = fields.Float(
        'Quantity',
        track_visibility='onchange',
        digits_compute=dp.get_precision(
        'Product Unit of Measure')
    )
    purchase_qty = fields.Float(
        'Purchase QTY',
        track_visibility='onchange',
        digits_compute=dp.get_precision(
        'Product Unit of Measure')
    )
    stock_qty = fields.Float(
        'Product from stock QTY',
        track_visibility='onchange',
        digits_compute=dp.get_precision(
        'Product Unit of Measure')
    )
    request_id = fields.Many2one(
        'stock.request',
        'Purchase Request',
        ondelete='cascade',
        readonly=True
    )
    company_id = fields.Many2one(
        'res.company',
        related='request_id.company_id',
        string='Company',
        store=True,
        readonly=True
    )
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        'Analytic Account',
        track_visibility='onchange'
    )
    requested_by = fields.Many2one(
        'res.users',
        related='request_id.requested_by',
        string='Requested by',
        store=True,
        readonly=True
    )
    assigned_to = fields.Many2one(
        'res.users',
        related='request_id.assigned_to',
        string='Assigned to',
        store=True,
        readonly=True
    )
    description = fields.Text(
        related='request_id.description',
        string='Description',
        readonly=True,
        store=True
    )
    origin = fields.Char(
        related='request_id.origin',
        size=32,
        string='Source Document',
        readonly=True,
        store=True
    )
    warehouse_id = fields.Many2one(
        'stock.warehouse',
        related='request_id.warehouse_id',
        string='Warehouse',
        store=True,
        readonly=True
    )
    date_required = fields.Date(
        string='Request Date',
        required=True,
        track_visibility='onchange',
        default=lambda *args: time.strftime(
            '%Y-%m-%d %H:%M:%S')
    )
    request_state = fields.Selection(
        string='Request state',
        readonly=True,
        related='request_id.state',
        selection=_STATES,
        store=True
    )
    supplier_id = fields.Many2one(
        'res.partner',
        string='Preferred supplier',
        compute="_get_supplier"
    )
    customer_name = fields.Char(
        'Customer name',
        size=256,
    )
    cost_price = fields.Float(
        string='Standard Cost Price',
        digits=dp.get_precision('Product Price'),
        readonly=False,
    )
    unit_price = fields.Float(
        string='Standard Cost Price',
        digits=dp.get_precision('Product Price'),
        readonly=False,
    )
    is_editable = fields.Boolean(
        string='Is editable',
        compute="_get_is_editable",
        readonly=True
    )

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            name = self.product_id.name
            if self.product_id.code:
                name = '[%s] %s' % (name, self.product_id.code)
            if self.product_id.description_purchase:
                name += '\n' + self.product_id.description_purchase
            #self.product_uom_id = self.product_id.uom_id.id
            self.product_qty = 1
            self.cost_price = self.product_id.standard_price

    @api.onchange('cost_price')
    def onchange_cost_price(self):
        if self.product_id:
            self.cost_price = self.product_id.standard_price

    @api.onchange('product_id')
    def onchange_product_for_uom_id(self):
        if self.product_id:
            self.product_uom_id = self.product_id.uom_id.id

class StockRequestRemine(models.Model):
    _name = 'stock.request.remine'

    request_id = fields.Many2one(
        comodel_name="stock.request",
        string="Stock Request",
        required=False,
    )
    desc = fields.Char(
        string="Desc",
        required=True,
    )
    date_remine = fields.Date(
        string="Date Remind",
        required=True,
    )
    amount = fields.Float(
        string="Amount",
        required=True,
    )
    state = fields.Selection(
        string="state",
        selection=[
           ('wait', 'Wait'),
           ('done', 'Done'),
        ],
        required=False,
        default='wait',
    )

