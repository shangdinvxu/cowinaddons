# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Cowin_foudation(models.Model):
    _name = ''


    name = fields.Char(string=u'基金名称')

    project_id = fields.Many2one('cowin_project.cowin_project', string=u'项目')

    investment_amount = fields.Float(string=u'本次投资金额')
    ownership_interest = fields.Float(string=u'股份比例')

    round_financing = fields.Selection([(1, u'天使轮'), (2, u'A轮'), (3, u'B轮'), (4, u'C轮')],
                                       string=u'融资轮次', required=True, default=1)
