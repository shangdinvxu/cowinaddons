# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Cowin_hr(models.Model):
    _inherit = 'hr.employee'


    backup_person = fields.Char(string=u'联系人')
    relation_to_me = fields.Char(string=u'关系')
    identification_id_contract_person = fields.Char(string=u'身份证号')
    mobile_phone_backup_contract_person = fields.Char(string=u'联系电话')


class IrMenuExtend(models.Model):
    _inherit = 'ir.ui.menu'

    button_icon = fields.Char(string=u'按钮图标')

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        fields.append("button_icon")
        return super(IrMenuExtend, self).read(fields, load)

