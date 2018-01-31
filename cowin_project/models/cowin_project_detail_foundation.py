# -*- coding: utf-8 -*-
from odoo import models, fields, api


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

    # 计算股份比例
    @api.one
    @api.depends('the_amount_of_investment')
    def _calc_ownership_interest(self):

        round_entity = self.env['cowin.project.detail.round']
        foundation_entity = self.env['cowin.project.detail.foundation']

        round_financing_ids = round_entity.read_group([
            ('project_id', '=', self.round_id.project_id)], ['round_financing_id'], ['round_financing_id'], lazy=False)

        temp_ownership_interest = self.the_amount_of_investment / (self.round_id.project_valuation + self.round_id.the_amount_of_financing)

        for round_financing_id in round_financing_ids:
            if self.round_id.round_financing_id > round_financing_id:
                foundations = foundation_entity.sudo().search(['round_id', '=', round_financing_id])
                for foundation in foundations:
                    foundation.ownership_interest = round(
                        foundation.the_amount_of_investment /
                        (round_financing_id.project_valuation + round_financing_id.the_amount_of_financing), 4)

            if self.round_id.round_financing_id < round_financing_id:
                temp_ownership_interest = round(
                    temp_ownership_interest * (
                        round_financing_id.project_valuation /
                        (round_financing_id.project_valuation + round_financing_id.the_amount_of_financing)), 4)

        self.ownership_interest = round(temp_ownership_interest, 4)
