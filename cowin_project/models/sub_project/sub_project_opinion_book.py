# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Cowin_project_subproject_opinion_book(models.Model):

    '''
        立项意见书
    '''
    _name = 'cowin_project.sub_opinion_book'


    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    invest_manager = fields.Many2one(related='subproject_id.invest_manager', string=u'投资经理')
    date_of_project = fields.Date(string=u'立项日期')

    # ------  投资基金
    #
    # foundation_id = fields.Many2one(related='subproject_id.foundation_id', string=u'基金名称')
    # ratio_between_investments = fields.Float(related='subproject_id.ratio_between_investments', string=u'本次投资金额')
    # ownership_interest = fields.Float(related='subproject_id.ownership_interest', string=u'股份比例')
    # # round_financing_id = fields.Many2one('cowin_common.round_financing', related='subproject_id.round_financing_id', string=u'融资轮次')
    # financing_money = fields.Float(related='subproject_id.financing_money', string=u'本次融资额')
    # -------
    project_mumbers = fields.Many2many('hr.employee', string=u'项目小组成员')

    # examine_and_verify = fields.Char(string=u'审核校验', default=u'未开始审核')

    partner_opinion = fields.Text(string=u'项目合伙人表决意见')
    business_director_option = fields.Text(string=u'业务总监表决意见')
    policy_making_committee = fields.Text(string=u'投资决策委员会意见')



