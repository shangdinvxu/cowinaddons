# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Cowin_foundation(models.Model):
    _name = 'cowin_foundation.cowin_foundation'

    '''
        基金信息
    '''

    manage_company_id = fields.Many2one('cowin_foudation.management_company', string=u'管理公司')

    intermediary_id = fields.Many2one('cowin_foudation.intermediary_info', string=u'中介机构情况')

    settings_id = fields.Many2one('cowin_foudation.settings', string=u'设置')

    sponsor_ids = fields.One2many('cowin_foudation.sponsor', 'foundation_id', string=u'出资人信息')

    partner_gp_ids = fields.One2many('cowin_foudation.sponsor_gp', 'foundation_id', string=u'GP(普通合伙)信息')

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



    @api.multi
    def get_formview_id(self):
        """ Return an view id to open the document ``self`` with. This method is
            meant to be overridden in addons that want to give specific view ids
            for example.
        """
        if len(self) > 1:
            raise UserWarning(u'只能最多有一个实体')

        form_id = self.env.ref('cowin_foundation.cowin_foundation_form').id

        return form_id





    @api.multi
    def _get_info(self):
        '''
            获得基金里面完整的完整的详细的信息
        :return:  info
        '''
        self.ensure_one()

        res = {}

        res['foundation_info'] = self.get_foundation_info()

        res['sponsor_info'] = self.get_sponsor_info()

        res['sponsor_gp_info'] = self.get_partner_gp_info()

        res['management_company_info'] = self.get_management_company_info()

        res['intermediary_info'] = self.get_intermediary_info()

        res['settings_info'] = self.get_settings_info()

        return {'foundation_full_info': res}



    @api.multi
    def get_foundation_info(self):

        self.ensure_one()

        return self.copy_data()

    @api.multi
    def get_sponsor_info(self):
        self.ensure_one()

        return self.sponsor_ids.get_sponsor_info()

    @api.multi
    def get_partner_gp_info(self):
        self.ensure_one()

        return self.partner_gp_ids.get_partner_gp_info()

    @api.multi
    def get_management_company_info(self):
        self.ensure_one()

        return self.manage_company_id.get_management_company_info()

    @api.multi
    def get_intermediary_info(self):
        self.ensure_one()

        return self.intermediary_id.get_intermediary_info()

    @api.multi
    def get_settings_info(self):
        self.ensure_one()

        return self.settings_id.get_settings_info()


    @api.multi
    def rpc_get_full_info(self):
        '''
            添加前端rpc调用接口的操作
        :return:
        '''
        self.ensure_one()

        return self._get_info()