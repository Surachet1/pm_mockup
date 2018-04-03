# -*- coding: utf-8 -*-
from openerp import api, fields, models

class Partner(models.Model):
    _inherit = "res.partner"

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
