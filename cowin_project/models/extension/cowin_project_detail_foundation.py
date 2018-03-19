# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Cowin_project_detail_foundation(models.Model):
    _name = 'cowin.project.detail.foundation'

    round_id = fields.Many2one('cowin.project.detail.round', string=u'详情轮次', ondelete='cascade')

    meta_sub_project_id = fields.Many2one('cowin_project.meat_sub_project', string=u'元子工程ID')

    ownership_interest = fields.Float(string=u'股份比例', compute="_calc_ownership_interest")

    the_amount_of_investment = fields.Float(string=u'本次投资金额')

    foundation = fields.Char(string=u'基金')

    data_from = fields.Selection([
        ('local', 'Local'),
        ('external', 'External')
    ], string='数据来源', default='local')

    withdrawal_ids = fields.One2many('cowin.project.detail.withdrawals', 'foundation_id', ondelete="cascade")

    _sql_constraints = [
        ('cowin_project_detail_foundation_project_unique', 'unique (round_id, meta_sub_project_id)', u"子项目轮次不可重复"),
    ]

    # 计算股份比例
    def _calc_ownership_interest(self):
        print 'sss'
        round_entity = self.env['cowin.project.detail.round']
        for self_one in self:
            rounds = round_entity.search([('project_id', '=', self_one.round_id.project_id.id)])

            temp_ownership_interest = self_one.the_amount_of_investment / (
                self_one.round_id.project_valuation + self_one.round_id.the_amount_of_financing)

            for round_ in rounds:
                if self_one.round_id.round_financing_id.sequence < round_.round_financing_id.sequence:
                    temp_ownership_interest = temp_ownership_interest * (
                        round_.project_valuation / (round_.project_valuation + round_.the_amount_of_financing))

            self_one.ownership_interest = round(temp_ownership_interest, 4)
