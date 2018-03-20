# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Cowin_foundation_GP(models.Model):
    _name = 'cowin_foudation.sponsor_gp'

    '''
        GP(普通合伙)信息
    '''

    name = fields.Char(string=u'GP名称')

    foundation_id = fields.Many2one('cowin_foundation.cowin_foundation', string=u'基金')

    registered_address = fields.Char(string=u'注册地址')

    capital_contribution = fields.Float(string=u'出资金额(万元)')

    capital_ratio = fields.Float(string=u'出资比例')

    amount_of_payment = fields.Float(string=u'实缴金额(万元)')

    amount_of_payment_ratio = fields.Float(string=u'实缴比例')

    the_nature_of_the_investor = fields.Selection([(1, u'国有'), (2, u'民营'), (3, u'外资')], string=u'出资人性质')

    institutional_investor = fields.Selection([(1, u'是'), (0, u'不是')], string=u'是否为投资机构')

    mailing_address_of_shareholders = fields.Char(string=u'股东邮寄地址')

    contract_person = fields.Char(string=u'联系人')

    contract_phone = fields.Char(string=u'联系电话')

    ID_number = fields.Char(string=u'证件号码')

    contract_email = fields.Char(string=u'Email')

    _sql_constraints = [
        ('name_key', 'UNIQUE (name)', u'出资人名称不能够相同')
    ]




    @api.multi
    def get_partner_gp_info(self):
        if self:
            return self.copy_data()