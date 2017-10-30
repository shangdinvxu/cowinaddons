# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Cowin_project_opinion_book(models.Model):
    _name = 'cowin_project.cowin_project_opinion_book'

    project_id = fields.Many2one('cowin_project.cowin_project')
    name = fields.Char(related='project_id.name')
    project_number = fields.Char(related='project_id.project_number')
    invest_manager = fields.Many2one(related='project_id.invest_manager')
    founding_time = fields.Date(related='project_id.founding_time')

    project_mumbers = fields.Many2many('hr.employee', string=u'项目小组成员')

    partner_opinion = fields.Text(string=u'项目合伙人表决意见')
    business_director_option = fields.Text(string=u'业务总监表决意见')
    business_director_option = fields.Text(string=u'投资决策委员会意见')

