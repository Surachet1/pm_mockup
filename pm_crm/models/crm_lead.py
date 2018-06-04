# -*- coding: utf-8 -*-

import logging
import werkzeug
import json
import base64
import re

# import openerp
# from openerp.addons.auth_signup.res_users import SignupError
# from openerp.addons.web.controllers.main import ensure_db
# from openerp import http
# from openerp.http import request
from openerp.tools.translate import _
from odoo.tools.safe_eval import safe_eval
from openerp import api, fields, models


class CrmLead(models.Model):

    _inherit = 'crm.lead'

    manager_id = fields.Many2one('res.users', string='Sales manager')
    lead_type = fields.Selection([
        ('om', 'OM'),
        ('hc', 'HC'),
    ],
    string="หน่วยงาน")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ],
    string="Gender")
    department = fields.Selection([
        ('om', 'OM'),
        ('hc', 'HC'),
        ('bc', 'BC'),
    ],
    string="หน่วยงาน")
    source_op = fields.Selection([
        ('phone', 'phone'),
        ('line', 'Line'),
        ('line_at', 'Line@'),
        ('email', 'Email'),
        ('direct', 'Direct'),
        ('hotline', 'Hot line'),
        ('fb', 'FB'),
        ('referal', 'Referal'),
        ('website', 'Website'),
    ],
    string="ที่มาของโอกาสการขาย")
    house_type = fields.Selection([
        ('hotel', 'โรงแรม'),
        ('apartment', 'apartment'),
        ('school', 'สถานศีกษา'),
        ('factory', 'โรงงาน'),
        ('hospital', 'โรงพยาบาล'),
        ('private', 'เอกชน'),
        ('gov', 'หน่วยงานราชการ'),
        ('airport', 'สนามบิน'),
        ('store', 'ห้างสรรพสินค้า'),
    ],
    string="ประเภทที่อยู่อาศัย")
    no_maid = fields.Integer('จำนวนแม่บ้าน')
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
    location_sign = fields.Char('สถานที่ทำสัญญา')
    location_send = fields.Char('ที่อยู่สำหรับการจัดส่งอุปกรณ์')
    no_service = fields.Integer('จำนวนครั้งที่เข้ารับบริการ')
    freq_service = fields.Integer('ความถี่ในการเข้ารับบริการ')
    time_service = fields.Integer('เวลาในการเข้ารับบริการ')

    house_type = fields.Selection([
        ('single', 'บ้านเดี่ยว'),
        ('town', 'ทาวน์โฮม'),
        ('commerce', 'อาคารพาณิชย์'),
        ('condo', 'คอนโด'),
        ('office', 'สำนักงาน'),
        ('other', 'อื่นๆ'),
    ],
    string="ประเภทที่อยู่อาศัย")
    no_floor = fields.Integer('จำนวนชั้น')
    no_toilet = fields.Integer('จำนวนห้องน้ำ')
    no_space = fields.Integer('จำนวนพื้นที่ใช้สอย')
    no_living = fields.Integer('จำนวนห้องนั่งเล่น')
    no_bedroom = fields.Integer('จำนวนห้องนอน')
    caution = fields.Char('ข้อควรระวัง')
    other_type = fields.Char('ระบุ')
    partner_service_id = fields.Many2one(
        'res.partner',
        string="ที่อยู่สำหรับให้บริการ",
    )
    distance = fields.Float('ระยะทาง(กม.)')
    latitude = fields.Float('ละติจูด')
    longitude = fields.Float('ลองจิจูด')

    @api.model
    def action_revise(self):
        return True

class Team(models.Model):
    _inherit = 'crm.team'

    @api.model
    def action_your_pipeline_hc(self):
        action = self.env.ref('crm.crm_lead_opportunities_tree_view').read()[0]
        user_team_id = self.env.user.sale_team_id.id
        action['domain'] = [('type','=','opportunity'),('lead_type','=','hc')]
        if not user_team_id:
            user_team_id = self.search([], limit=1).id
            action['help'] = """<p class='oe_view_nocontent_create'>Click here to add new opportunities</p><p>
    Looks like you are not a member of a sales team. You should add yourself
    as a member of one of the sales team.
</p>"""
            if user_team_id:
                action['help'] += "<p>As you don't belong to any sales team, Odoo opens the first one by default.</p>"

        action_context = safe_eval(action['context'], {'uid': self.env.uid})
        action_context['default_lead_type'] = 'hc'
        action_context['default_department'] = 'hc'
        if user_team_id:
            action_context['default_team_id'] = user_team_id

        tree_view_id = self.env.ref('crm.crm_case_tree_view_oppor').id
        form_view_id = self.env.ref('crm.crm_case_form_view_oppor').id
        kanb_view_id = self.env.ref('crm.crm_case_kanban_view_leads').id
        action['views'] = [
                [kanb_view_id, 'kanban'],
                [tree_view_id, 'tree'],
                [form_view_id, 'form'],
                [False, 'graph'],
                [False, 'calendar'],
                [False, 'pivot']
            ]
        action['context'] = action_context
        return action


    @api.model
    def action_your_pipeline_om(self):
        action = self.env.ref('crm.crm_lead_opportunities_tree_view').read()[0]
        user_team_id = self.env.user.sale_team_id.id
        action['domain'] = [('type','=','opportunity'),('lead_type','=','om')]
        if not user_team_id:
            user_team_id = self.search([], limit=1).id
            action['help'] = """<p class='oe_view_nocontent_create'>Click here to add new opportunities</p><p>
    Looks like you are not a member of a sales team. You should add yourself
    as a member of one of the sales team.
</p>"""
            if user_team_id:
                action['help'] += "<p>As you don't belong to any sales team, Odoo opens the first one by default.</p>"

        action_context = safe_eval(action['context'], {'uid': self.env.uid})
        action_context['default_lead_type'] = 'om'
        action_context['default_department'] = 'om'
        if user_team_id:
            action_context['default_team_id'] = user_team_id

        tree_view_id = self.env.ref('crm.crm_case_tree_view_oppor').id
        form_view_id = self.env.ref('crm.crm_case_form_view_oppor').id
        kanb_view_id = self.env.ref('crm.crm_case_kanban_view_leads').id
        action['views'] = [
                [kanb_view_id, 'kanban'],
                [tree_view_id, 'tree'],
                [form_view_id, 'form'],
                [False, 'graph'],
                [False, 'calendar'],
                [False, 'pivot']
            ]
        action['context'] = action_context
        return action
