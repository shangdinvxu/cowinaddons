# -*- coding: utf-8 -*-
from odoo import models, fields, api

class sub_project_quarterly_analysis_report_on_investment_projects(models.Model):

    _name = 'cowin_project.sub_quarterly_analysis_report'


    '''
        投资项目季度分析报告

    '''

    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')


    a = fields.Many2one('hr.employee', string=u'报告人')

    b = fields.Datetime(string=u'提交日期')