# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, exceptions

class Employee(models.Model):
    _inherit = 'hr.employee'

    emp_history_ids = fields.One2many(
        comodel_name='hr.employee.history',
        inverse_name='emp_id',
        string='Hostory',
        help='Help note'
    )
    training_employee_ids = fields.One2many(
        "hr.employee.training",
        "emp_id",
        string="Training"
    )
    skill_ids = fields.One2many(
        "hr.skill",
        "emp_id",
        string="Skill"
    )


class HREmployeeHistory(models.Model):
    _name = 'hr.employee.history'
    _description = 'History Employee'

    emp_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employee',
    )
    name = fields.Char(
        string='ชื่อบริษัท',
        size=64,
    )
    start_date = fields.Date(
        string='วันที่เริ่มงาน',
    )
    end_date = fields.Date(
        string='วันที่ลาออก',
    )

class Training(models.Model):
    _name = "hr.employee.training"

    training_id = fields.Many2one(
        "hr.training",
        "Training",
        required=True
    )
    emp_id = fields.Many2one(
        "hr.employee",
        "Employee"
    )
    no_time = fields.Integer("Number of time")
    hours = fields.Integer("Number of Hours")
    date_issue = fields.Date('Date of Issue')
    date_expired = fields.Date('Date of expired')
    date_training_expired = fields.Date('Training Contract Expired')
   #purchase_order_id = fields.Many2one(
   #    comodel_name='purchase.order',
   #    string="Ref. Training Request"
   #)
    image = fields.Binary('File Training')

class HRSkill(models.Model):
    _name = 'hr.skill'
    _description = 'HR Skill'

    emp_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employee',
    )
    name = fields.Char(
        string='name',
        size=64,
    )
    rating = fields.Selection(
        selection=[
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
        ],
        string='Rating',
    )

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    plan_check_in = fields.Datetime(
        string='Planned Check In',
    )
    plan_check_out = fields.Datetime(
        string='Planned Check Out',
    )
