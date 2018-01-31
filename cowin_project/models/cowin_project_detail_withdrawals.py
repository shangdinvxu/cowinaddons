# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Cowin_project_detail_withdrawals(models.Model):

    _name = 'cowin.project.detail.withdrawals'

    foundation_id = fields.Many2one('cowin.project.detail.foundation', string=u'基金详情', ondelete='cascade')

    ownership_interest = fields.Float(string=u'股份比例')

    the_amount_of_withdrawals = fields.Float(string=u'本次投资金额')

    project_valuation = fields.Float(string=u'估值')
