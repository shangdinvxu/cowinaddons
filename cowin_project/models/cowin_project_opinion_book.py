# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Cowin_project_opinion_book(models.Model):
    _name = 'cowin_project.cowin_project_opinion_book'

    foundation_stage_id = fields.Many2one('cowin_project.cowin_foudation_stage', string=u'基金阶段')
    # project_number = fields.Char(related='project_id.project_number')
    # invest_manager = fields.Many2one(related='project_id.invest_manager')
    # founding_time = fields.Date(related='project_id.founding_time')
    # examine_and_verify = fields.Selection([(1, u'无'), (2, u'审核中'), (3, u'审核通过')],
    #                                       string=u'审核校验', required=True, default=1)

    examine_and_verify = fields.Char(string=u'审核校验', default=u'未开始审核')
    project_mumbers = fields.Many2many('hr.employee', string=u'项目小组成员')

    partner_opinion = fields.Text(string=u'项目合伙人表决意见')
    business_director_option = fields.Text(string=u'业务总监表决意见')
    policy_making_committee = fields.Text(string=u'投资决策委员会意见')

