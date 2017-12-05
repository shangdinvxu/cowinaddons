# -*- coding: utf-8 -*-
from odoo import models, fields, api

class sub_project_application_for_investment_withdrawal(models.Model):
    _name = 'cowin_project.sub_app_for_investment_withdrawal'


    '''
        投资退出申请书
    '''

    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    b = fields.Datetime(string=u'报告日期')

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


    a = fields.Many2one('hr.employee', string=u'董事')
    b = fields.Many2one('hr.employee', string=u'监事')
    c = fields.Float(string=u' 退出金额')
    d = fields.Float(string=u' 退出比例')

    e = fields.Many2many(string=u'决策文件清单')

    f = fields.Text(string=u'退出方案')