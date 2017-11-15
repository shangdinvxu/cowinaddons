# -*- coding: utf-8 -*-
from odoo import models, fields, api
class Cowin_project_subproject_payment_application_form(models.Model):
    '''
        付款申请表
    '''

    _name = 'cowin_project.sub_payment_app_form'

    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    invest_manager = fields.Many2one(related='subproject_id.invest_manager', string=u'投资经理')

    date_of_application = fields.Date(string=u'申请日期')


    list_of_examination_and_approval_documents = fields.Many2many('ir.attachment', string=u'审批文件')

    monetary_unit = fields.Char(string=u'货币单位')
    payment_amount = fields.Float(string=u'本期付款金额')
    total_investment = fields.Float(string=u'公司投资总额')

    number_of_periods = fields.Integer(string=u'付款期数')
    accumulated_payment_amount = fields.Float(string=u'累计付款金额')
    payment_amount = fields.Float(string=u'未付金额')

    payee_name = fields.Char(string=u'收款人名称')
    account_number = fields.Char(string=u'收款账号')
    bank_of_deposit = fields.Char(string=u'开户银行')
    funds_provided = fields.Char(string=u'资金来源')

    # ------  投资基金
    #
    # foundation_id = fields.Many2one(related='subproject_id.foundation_id', string=u'基金名称')
    # # ratio_between_investments = fields.Float(related='subproject_id.ratio_between_investments', string=u'本次投资金额')
    # ownership_interest = fields.Float(related='subproject_id.ownership_interest', string=u'股份比例')
    # round_financing_id = fields.Many2one('cowin_common.round_financing', related='subproject_id.round_financing_id', string=u'融资轮次')
    # financing_money = fields.Float(related='subproject_id.financing_money', string=u'本次融资额')

    # -------

    payment_account = fields.Char(string=u'付款账号')
