# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Cowin_project_detail_foundation(models.Model):
    _name = 'cowin.project.detail.foundation'

    round_id = fields.Many2one('cowin.project.detail.round', string=u'详情轮次', ondelete='cascade')

    ownership_interest = fields.Float(string=u'股份比例', compute="_calc_ownership_interest")

    the_amount_of_investment = fields.Float(string=u'本次投资金额')

    foundation = fields.Char(string=u'基金')

    data_from = fields.Selection([
        ('local', 'Local'),
        ('external', 'External')
    ], string='数据来源', default='local')

    # 计算股份比例
    @api.multi
    @api.depends('the_amount_of_investment')
    def _calc_ownership_interest(self):

        round_entity = self.env['cowin.project.detail.round']
        foundation_entity = self.env['cowin.project.detail.foundation']
        for s in self:
            rounds = round_entity.search([('project_id', '=', s.round_id.project_id.id)])

            temp_ownership_interest = s.the_amount_of_investment / (
            s.round_id.project_valuation + s.round_id.the_amount_of_financing)

            for round_ in rounds:
                if s.round_id.round_financing_id.sequence > round_.round_financing_id.sequence:
                    foundations = foundation_entity.sudo().search(['round_id', '=', round_.id])
                    for foundation in foundations:
                        foundation.ownership_interest = round(
                            foundation.the_amount_of_investment /
                            (round_.project_valuation + round_.the_amount_of_financing), 4)

                if s.round_id.round_financing_id.sequence < round_.round_financing_id.sequence:
                    temp_ownership_interest = round(
                        temp_ownership_interest * (
                            round_.project_valuation /
                            (round_.project_valuation + round_.the_amount_of_financing)), 4)

            s.ownership_interest = round(temp_ownership_interest, 4)
