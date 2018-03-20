# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Cowin_foundation_management_company(models.Model):
    _name = 'cowin_foudation.management_company'

    '''
        基金管理公司
    '''

    name = fields.Char(string=u'基金管理公司名称')

    foundation_ids = fields.One2many('cowin_foundation.cowin_foundation', 'manage_company_id', string=u'基金')

    management_company_adress = fields.Char(string=u'基金管理公司通讯地址')

    zip_code = fields.Char(string=u'邮编')

    management_company_chairman = fields.Char(string=u'基金管理公司董事长(或者创始人)')

    contract_phone_for_chairman = fields.Char(string=u'联系电话(手机/座机/传真)')

    management_company_manager = fields.Char(string=u'基金管理公司总经理(或者第二合伙人/第二负责人)')

    contract_phone_for_manager = fields.Char(string=u'联系电话(手机/座机/传真)')

    management_company_daily_contact = fields.Char(string=u'基金管理公司日常联系人')

    contract_phone_for_daily_contact = fields.Char(string=u'联系电话(手机/座机/传真)')



    @api.multi
    def get_management_company_info(self):
        self.ensure_one()

        return self.copy_data()