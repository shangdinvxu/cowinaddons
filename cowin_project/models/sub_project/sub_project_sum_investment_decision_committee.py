# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Cowin_project_subproject_sum_investment_decision_committee(models.Model):
    '''
        投资决策委员会会议纪要
    '''

    _name = 'cowin_project.sub_sum_invest_decision_committee'

    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    invest_manager = fields.Many2one(related='subproject_id.invest_manager', string=u'投资经理')

    voting_committee_date = fields.Date(string=u'投决会日期')

    conference_recorder = fields.Many2one('hr.employee', string=u'会议记录人')
    checker = fields.Many2one('hr.employee', string=u'复核人')
    investment_decision_committee = fields.Many2many('hr.employee', string=u'投资决策委员')

    conference_highlights = fields.Text(string=u'会议要点')

