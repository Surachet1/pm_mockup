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
 
from openerp import api, fields, models
 
 
class CrmLead(models.Model):
 
    _inherit = 'crm.lead'

    manager_id = fields.Many2one('res.users', string='Sales manager')
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

