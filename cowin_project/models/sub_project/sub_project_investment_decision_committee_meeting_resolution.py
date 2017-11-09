# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Cowin_project_subprojec_investment_decision_committee_meeting_resolution(models.Model):

    '''
        投资决策委员会会议决议
    '''
    _name = 'cowin_project.sub_invest_decision_committee_res'

    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    invest_manager = fields.Many2one(related='subproject_id.invest_manager', string=u'投资经理')

    voting_committee = fields.Date(string=u'投决会日期')
    outcome_of_the_voting_committee = fields.Char(string=u'投决会结果')

    # ------  投资基金

    foundation_id = fields.Many2one(related='subproject_id.foundation_id', string=u'基金名称')
    ratio_between_investments = fields.Float(related='subproject_id.ratio_between_investments', string=u'本次投资金额')
    ownership_interest = fields.Float(related='subproject_id.ownership_interest', string=u'股份比例')
    round_financing_id = fields.Many2one('cowin_common.round_financing', related='subproject_id.round_financing_id', string=u'融资轮次')
    financing_money = fields.Float(related='subproject_id.financing_money', string=u'本次融资额')

    # -------


    trustee = fields.Many2one('hr.employee', string=u'董事')
    supervisor = fields.Many2one('hr.employee', string=u'监事')
    amount_of_entrusted_loan = fields.Float(string=u'委托贷款金额')
    chairman_of_investment_decision_committee = fields.Many2one('hr.employee', string=u'投资决策委员会主席')

