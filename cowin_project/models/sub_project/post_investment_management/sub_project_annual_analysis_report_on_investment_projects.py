# -*- coding: utf-8 -*-
from odoo import models, fields, api

class sub_project_annual_analysis_report_on_investment_projects(models.Model):
    _name = 'cowin_project.sub_annual_analysis_report_on_invest_pros'

    '''
        投资项目年度分析报告
    '''

    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')

    a = fields.Many2one('报告人', string=u'报告人')

    b = fields.Datetime(string=u'提交日期')

    registered_address = fields.Char(string=u'注册地')

    e = fields.Many2one('hr.employee', string=u'董事长')

    c = fields.Many2one('hr.employee', string=u'总经理')

    c1 = fields.Text(string=u'产品')

    c2 = fields.Many2one('', string=u'所属行业')

    c3 = fields.Date(string=u'成立时间')


    c4 = fields.Char(string=u'投资阶段')

    c5 = fields.Char(string=u'当前阶段')

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


    e1 = fields.Float(string=u'总资产')
    e2 = fields.Float(string=u'总负债')
    trustee = fields.Many2one('hr.employee', string=u'董事')

    e3 = fields.Char(string=u'券商')

    e4 = fields.Text(string=u'IPO计划')

    e5 = fields.Text(string=u'公司现状')

    e6 = fields.Text(string=u'行业现状')