# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Cowin_project_subproject_investment_decision_application(models.Model):

    '''
        投资决策申请
    '''

    _name = 'cowin_project.sub_invest_decision_app'

    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    invest_manager = fields.Many2one(related='subproject_id.invest_manager', string=u'投资经理')

    # ------  投资基金

    foundation_id = fields.Many2one(related='subproject_id.foundation_id', string=u'基金名称')
    ratio_between_investments = fields.Float(related='subproject_id.ratio_between_investments', string=u'本次投资金额')
    ownership_interest = fields.Float(related='subproject_id.ownership_interest', string=u'股份比例')
    round_financing_id = fields.Many2one('cowin_common.round_financing', related='subproject_id.round_financing_id', string=u'融资轮次')
    financing_money = fields.Float(related='subproject_id.financing_money', string=u'本次融资额')

    # -------

    company_investment_role = fields.Selection([(1, u'单一投资人'), (2, u'主导投资人'), (3, u'跟投')],
                                               string=u'本公司的投资角色')

    decision_file_list = fields.Many2many('ir.attachment', string=u'决策文件清单')

    investment_decision_Committee_held_time = fields.Date(string=u'投资决策委员会召开时间')

