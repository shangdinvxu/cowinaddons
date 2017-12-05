# -*- coding: utf-8 -*-
from odoo import models, fields, api

class sub_project_project_exit_resolution(models.Model):

    _name = 'cowin_project.sub_project_exit_resolution'

    '''
        项目退出决议
    '''

    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    invest_manager_id = fields.Many2one('hr.employee', related='subproject_id.invest_manager_id', string=u'投资经理')

    project_exit_date = fields.Date(string=u'项目退出会议日期')

    result = fields.Char(string=u'项目退出会议结果')

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


    withdrawal_amount = fields.Float(string=u'退出金额')
    withdrawal_ratio = fields.Float(string=u'退出比例')
    exit_plan = fields.Text(string=u'退出方案')

    chairman_of_investment_decision_committee = fields.Many2one('hr.employee', string=u'投资决策委员会主席')