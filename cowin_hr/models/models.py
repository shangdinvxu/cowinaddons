# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Cowin_hr(models.Model):
    _inherit = 'hr.employee'


    backup_person = fields.Char(string=u'联系人')
    relation_to_me = fields.Char(string=u'关系')
    identification_id_contract_person = fields.Char(string=u'身份证号')
    mobile_phone_backup_contract_person = fields.Char(string=u'联系电话')

    barcode = fields.Char(string=u'员工编码')

    is_add_user=fields.Boolean()
    login_name=fields.Char()
    # login = fields.Char(related='user_id.login')




    @api.model
    def create(self, vals):
        if not vals.get('barcode'):
            vals['barcode'] = self.env['ir.sequence'].next_by_code('cowin_hr.order')


        # 创建当前的hr.employee实例
        res_hr=super(Cowin_hr, self).create(vals)


        # # 开始对外键进行设置
        if vals.get('login_name'):
            # 这样的命名的规则是从字段的命名规则来考虑
            user_id=self.env['res.users'].create({
                'login_name': 'nam',
                'pass':'123455'

            })

            res_hr.user_id=user_id.id
            res_hr.address_home_id=user_id.partner_id.id
        return res


