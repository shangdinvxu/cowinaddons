# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Cowin_hr(models.Model):
    _inherit = 'hr.employee'


    backup_person = fields.Char(string=u'备用联系人')
    relation_to_me = fields.Char(string=u'与本人的关系')
    identification_id_contract_person = fields.Char(string=u'备用联系人身份证号')
    mobile_phone_backup_contract_person = fields.Char(string=u'备用联系人联系电话')



