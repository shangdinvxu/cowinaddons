# -*- coding: utf-8 -*-
from odoo import models, fields, api


class sub_project_summary_of_the_project_withdrawal_from_the_meeting(models.Model):
    _name = 'cowin_project.sub_sum_pro_withdraw_from_meeting'

    '''
        项目退出会议纪要

    '''

    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    invest_manager_id = fields.Many2one('hr.employee', related='subproject_id.invest_manager_id', string=u'投资经理')

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
    conference_recorder = fields.Many2one('hr.employee', string=u'会议记录人')
    checker = fields.Many2one('hr.employee', string=u'复核人')
    investment_decision_committee = fields.Many2many('hr.employee', string=u'投资决策委员')

    conference_highlights = fields.Text(string=u'会议要点')