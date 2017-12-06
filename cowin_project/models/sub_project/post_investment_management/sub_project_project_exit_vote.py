# -*- coding: utf-8 -*-

from odoo import models, fields, api

class sub_project_project_exit_vote(models.Model):
    _name = 'cowin_project.sub_exit_vote'

    '''
        项目退出会议表决票
    '''

    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')

    # ----------  投资基金
    round_financing_id = fields.Many2one('cowin_common.round_financing',
                                         related='subproject_id.round_financing_id', string=u'轮次')

    foundation_id = fields.Many2one('cowin_foundation.cowin_foudation',
                                    related='subproject_id.foundation_id', string=u'基金')

    the_amount_of_financing = fields.Float(
        related='subproject_id.the_amount_of_financing', string=u'本次融资额')

    the_amount_of_investment = fields.Float(
        related='subproject_id.the_amount_of_investment', string=u'本次投资金额')
    ownership_interest = fields.Integer(
        related='subproject_id.ownership_interest', string=u'股份比例')
    # ---------------

    conference_date = fields.Date(string=u'会议日期')
    investment_decision_committee = fields.Many2many('hr.employee', string=u'投资决策委员')
    voting_opinion = fields.Text(string=u'表决意见')
    voter = fields.Char('hr.employee', string=u'表决人')