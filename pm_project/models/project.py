from odoo import api, fields, models, _, exceptions

class Project(models.Model):

    _inherit = 'project.project'
    _description = 'Project'

    project_list_ids = fields.One2many(
        "project.project.line",
        "project_id",
        string="Technician List",
        required=False,
    )

    project_estimate_ids = fields.One2many(
        "project.project.estimate",
        "project_id",
        string="Projrct Estimate Budget",
        required=False,
    )

    amount_total = fields.Float(
        compute="_compute_amount",
        string="Amount",
        track_visibility='onchange',
    )

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
