# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Cowin_foundation_intermediary_info(models.Model):
    _name = 'cowin_foundation.intermediary_info'

    '''
        中介机构情况
    '''

    name = fields.Char(string=u'托管银行')

    node_base_id = fields.Many2one('cowin_foundation.meta_foundation', string=u'基本节点', ondelete='cascade')

    # foundation_id = fields.Many2one('cowin_foundation.cowin_foundation', string=u'基金')
    foundation_ids = fields.One2many('cowin_foundation.cowin_foundation', 'intermediary_id', string=u'基金')

    trustee_bank_adress = fields.Char(string=u'托管银行地址')

    contract_person_for_trustee_bank = fields.Char(string=u'联系人')

    contract_phone_for_trustee_bank = fields.Char(string=u'联系电话')

    auditing_offices = fields.Char(string=u'审计机构')

    auditing_offices_adress = fields.Char(string=u'审计机构地址')

    contract_person_for_auditing_offices= fields.Char(string=u'联系人')

    contract_phone_for_auditing_offices = fields.Char(string=u'联系电话')


    @api.multi
    def get_intermediary_info(self):
        if len(self) == 1:
            return self.copy_data()[0]

    @api.multi
    def button_save(self):
        '''
            这个方法不要调用,原理在于每次button调用之前都会提前走write方法!!!
        :return:
        '''
        # self.ensure_one()

        pass