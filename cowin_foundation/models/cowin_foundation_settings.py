# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Cowin_foundation_settings(models.Model):
    _name = 'cowin_foudation.settings'

    '''
        基金配置信息
    '''

    name = fields.Many2one('hr.employee', string=u'基金专员')

    foundation_id = fields.Many2one('cowin_foundation.cowin_foundation', string=u'基金')
    # name = fields.Char()




