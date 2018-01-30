# -*- coding: utf-8 -*-
from odoo import models, fields


class Cowin_project_detail(models.Model):

    _name = 'cowin.project.detail'

    project_id = fields.Many2one('cowin_project.cowin_project', string='Project', ondelete='restrict')

    round_financing_id = fields.Many2one('cowin_common.round_financing', string=u'融资轮次')

    the_amount_of_financing = fields.Float(string=u'本次融资额')

    ownership_interest = fields.Float(string=u'股份比例')

    the_amount_of_investment = fields.Float(string=u'本次投资金额')

    foundation = fields.Char(string=u'基金')

    project_valuation = fields.Float(string=u'估值')

    data_from = fields.Selection([
        ('local', 'Local'),
        ('external', 'External')
    ], string='数据来源', default='local')
