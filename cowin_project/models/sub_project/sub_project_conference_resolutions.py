# -*- coding: utf-8 -*-

from odoo import models, fields, api
class Cowin_project_subproject_conference_resolutions(models.Model):
    '''
        投资决策委员会会议表决票
    '''

    _name = 'cowin_project.conference_resolutions'

    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    invest_manager = fields.Many2one(related='subproject_id.invest_manager', string=u'投资经理')

    voting_committee = fields.Date(string=u'投决会日期')

    members_of_voting_committee = fields.Many2many('hr.employee', string=u'投决会委员')

    voting_opinion = fields.Text(string=u'表决意见')

    voter = fields.Char(string=u'表决人')