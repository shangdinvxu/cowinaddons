# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Cowin_foundation_settings(models.Model):
    _name = 'cowin_foudation.settings'

    '''
        基金配置信息
    '''

    name = fields.Many2one('hr.employee', string=u'基金专员')

    node_base_id = fields.Many2one('cowin_foudation.node_base', string=u'基本节点')

    foundation_id = fields.One2many('cowin_foundation.cowin_foundation', 'settings_id', string=u'基金')
    # name = fields.Char()




    @api.multi
    def get_settings_info(self):
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