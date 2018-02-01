# -*- coding: utf-8 -*-
from odoo import models, fields


class Cowin_project_detail_foundation(models.Model):

    _name = 'cowin.project.detail.foundation'

    round_id = fields.Many2one('cowin.project.detail.round', string=u'详情轮次', ondelete='cascade')

    ownership_interest = fields.Float(string=u'股份比例')

    the_amount_of_investment = fields.Float(string=u'本次投资金额')

    foundation = fields.Char(string=u'基金')

    data_from = fields.Selection([
        ('local', 'Local'),
        ('external', 'External')
    ], string='数据来源', default='local')
