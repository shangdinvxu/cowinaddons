# -*- coding: utf-8 -*-
from odoo import models, fields, api
class Cowin_project_subproject_project_data_archiving(models.Model):

    '''
        项目资料归档
    '''

    _name = 'cowin_project.sub_project_data_archiving'



    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    invest_manager = fields.Many2one(related='subproject_id.invest_manager', string=u'投资经理')

    a = fields.Char(string=u'项目合伙人')

    # ------  投资基金

    # foundation_id = fields.Many2one(related='subproject_id.foundation_id', string=u'基金名称')
    # ratio_between_investments = fields.Float(related='subproject_id.ratio_between_investments', string=u'本次投资金额')
    # ownership_interest = fields.Float(related='subproject_id.ownership_interest', string=u'股份比例')
    # round_financing_id = fields.Many2one('cowin_common.round_financing', related='subproject_id.round_financing_id', string=u'融资轮次')
    # financing_money = fields.Float(related='subproject_id.financing_money', string=u'本次融资额')

    # -------


    investment_decision_process_information = fields.Many2many('ir.attachment', string=u'投资决策流程资料')
    relevant_legal_documents_and_materials = fields.Many2many('ir.attachment', string=u'相关法律文件资料')
    government_approval_materials = fields.Many2many('ir.attachment', string=u'政府审批资料')
    payment_process_information = fields.Many2many('ir.attachment', string=u'付款流程资料')
    business_change_data = fields.Many2many('ir.attachment', string=u'工商变更资料')