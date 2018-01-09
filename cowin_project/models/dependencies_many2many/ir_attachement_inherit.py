# -*- coding: utf-8 -*-
from odoo import models, fields, api

class cowin_project_attachment_rel(models.Model):
    _inherit = 'ir.attachment'

    # 主工程
    project_ids = fields.Many2many('cowin_project.cowin_project', 'cowin_project_attachment_rel')
    #
    # # 子工程
    sub_project_ids = fields.Many2many('cowin_project.cowin_subproject', 'cowin_subproject_attachment_rel')
    #
    # # 尽调报告
    subt_dispatch_report_ids = fields.Many2many('cowin_project.subt_dispatch_report', 'subt_dispatch_report_attachment_rel')
    #
    # # 投资决策申请
    sub_invest_decision_app_ids = fields.Many2many('cowin_project.sub_invest_decision_app', 'sub_invest_decision_app_attachment_rel')
    #
    # # 项目出资申请表
    sub_app_form_pro_investment_ids = fields.Many2many('cowin_project.sub_app_form_pro_investment', 'sub_app_form_pro_investment_attachment_rel')
    #
    # # 项目委托贷款申请表
    sub_entrusted_loan_app_form_ids = fields.Many2many('cowin_project.sub_entrusted_loan_app_form', 'sub_entrusted_loan_app_form_attachment_rel')
    #
    # # 付款申请表
    sub_payment_app_form_ids = fields.Many2many('cowin_project.sub_payment_app_form', 'sub_payment_app_form_attachment_rel')
    #
    #
    # # 项目资料归档
    investment_decision_process_information_ids = fields.Many2many('cowin_project.sub_project_data_archiving', 'investment_decision_process_information_attachment_rel')
    relevant_legal_documents_and_materials_ids = fields.Many2many('cowin_project.sub_project_data_archiving', 'relevant_legal_documents_and_materials_attachment_rel')
    government_approval_materials_ids = fields.Many2many('cowin_project.sub_project_data_archiving', 'government_approval_materials_attachment_rel')
    payment_process_information_ids = fields.Many2many('cowin_project.sub_project_data_archiving', 'payment_process_information_attachment_rel')
    business_change_data_ids = fields.Many2many('cowin_project.sub_project_data_archiving', 'business_change_data_attachment_rel')
    #
    # # 投资退出申请书
    sub_app_invest_withdrawal_ids = fields.Many2many('cowin_project.sub_app_invest_withdrawal', 'sub_app_invest_withdrawal_attachment_rel')










