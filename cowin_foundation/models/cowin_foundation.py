# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Cowin_foundation(models.Model):
    _name = 'cowin_foundation.cowin_foundation'

    '''
        基金信息
    '''

    manage_company_ids = fields.One2many('cowin_foudation.management_company', 'foundation_id', string='管理公司',)

    name = fields.Char(string=u'基金名称')

    foundation_number = fields.Char(string=u'基金编号')

    registered_address = fields.Char(string=u'注册地址')

    foundation_type = fields.Selection([(1, u'天使基金'), (2, u'VC基金'), (3, u'PE基金')], string=u'基金类型')

    investment_field = fields.Many2many('cowin_common.cowin_industry', 'cowin_foudation_cowin_industry_rel', string=u'投资领域')

    term_of_investment = fields.Float(string=u'投资期限(年)')

    start_date_of_investment = fields.Date(string=u'投资起始日')

    registered_foundation_date = fields.Date(string=u'基金注册时间')

    first_investment_time_of_the_fund = fields.Date(string=u'基金首期出资时间')

    fund_investment_amonut = fields.Float(string=u'基金投资金额(万元)')

    securities_account = fields.Char(string=u'证券账户')

    fund_recognition_scale = fields.Float(string=u'基金认缴规模(万元)')

    funds_in_place_at_present_amount = fields.Float(string=u'目前基金到位资金额(万元)')

    funds_in_place_at_present_ratio= fields.Float(string=u'目前基金到位资金比率')

    state_investor_commitment_capital_con_amount = fields.Float(string=u'国有出资人承诺出资(万元)')

    current_state_investor_commitment_capital_con_amount = fields.Float(string=u'目前国有出资人承诺出资(万元)')

    current_state_investor_commitment_capital_con_amount_ratio = fields.Float(string=u'目前国有出资人到位比率')

    commitment_con_by_social_contributors_amount = fields.Float(string=u'社会出资人承诺出资(万元)')

    current_commitment_con_by_social_contributors_amount = fields.Float(string=u'目前社会出资人到位资金额(万元)')

    current_commitment_con_by_social_contributors_amount_ratio = fields.Float(string=u'目前社会出资人到位比率')

    team_commitment_capital_con_amount_GP = fields.Float(string=u'GP团队承诺出资(万元)')

    current_team_commitment_capital_con_amount_GP = fields.Float(string=u'GP团队到位资金额(万元)')

    current_team_commitment_capital_con_amount_GP_ratio = fields.Float(string=u'目前GP团队到位比率')

    fund_raising_report_ids = fields.Many2many('ir.attachment', 'cowin_foudation_fund_raising_report_rel', string=u'基金募资报告')

    fund_record_certificate_ids = fields.Many2many('ir.attachment', 'cowin_foudation_fund_record_certificate_rel', string=u'基金备案证书')

    agreement_ids = fields.Many2many('ir.attachment', 'cowin_foudation_agreement_rel', string=u'协议')

    government_approval_materials_ids = fields.Many2many('ir.attachment', 'cowin_foudation_government_approval_materials_rel', string=u'政府审批材料')

    semi_annual_report_of_the_fund_ids = fields.Many2many('ir.attachment', 'cowin_foudation_semi_annual_report_of_the_fund_rel', string=u'基金半年度报告')





    _sql_constraints = [
        ('name_key', 'UNIQUE (name)', u'基金名不能够相同')
    ]



