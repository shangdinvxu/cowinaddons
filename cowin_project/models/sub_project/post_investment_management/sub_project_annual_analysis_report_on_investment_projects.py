# -*- coding: utf-8 -*-
from odoo import models, fields, api

class sub_project_annual_analysis_report_on_investment_projects(models.Model):
    _name = 'cowin_project.sub_annual_analysis_report_on_invest_pros'

    '''
        投资项目年度分析报告
    '''

    subproject_id = fields.Many2one('cowin_project.cowin_subproject', ondelete="cascade")

    # name = fields.Char(related='subproject_id.name', string=u"项目名称")
    # project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')

    name = fields.Char(string=u"项目名称")
    project_number = fields.Char(string=u'项目编号')

    reporter = fields.Many2one('hr.employee', string=u'报告人')

    filing_date = fields.Date(string=u'提交日期')

    registered_address = fields.Char(string=u'注册地')

    chairman = fields.Many2one('hr.employee', string=u'董事长')

    general_manager = fields.Many2one('hr.employee', string=u'总经理')

    product = fields.Text(string=u'产品')

    industry = fields.Many2one('cowin_common.cowin_industry', string=u'所属行业')

    founding_time = fields.Date(string=u'成立时间')

    investment_phase = fields.Selection([(1, u'种子期'), (2, u'成长早期'), (3, u'成长期'), (4, u'成熟期')], string=u'投资阶段',
                                        default=1)
    current_phase = fields.Selection([(0, u'种子期'), (1, u'成长早期'), (2, u'成长期'), (3, u'成熟期')], string=u'当前阶段')

    # ----------  投资基金
    round_financing_and_foundation_id = fields.Many2one('cowin_project.round_financing_and_foundation',
                                                        related='subproject_id.round_financing_and_foundation_id',
                                                        string=u'基金轮次实体')
    round_financing_id = fields.Many2one('cowin_common.round_financing', string=u'融资轮次')
    foundation_id = fields.Many2one('cowin_foundation.cowin_foudation', string=u'基金名称')
    the_amount_of_financing = fields.Float(string=u'本次融资金额')
    the_amount_of_investment = fields.Float(string=u'本次投资金额')
    ownership_interest = fields.Integer(string=u'股份比例')

    # # ----------  投资基金
    # round_financing_id = fields.Many2one('cowin_common.round_financing',
    #                                      related='subproject_id.round_financing_id', string=u'轮次')
    #
    # foundation_id = fields.Many2one('cowin_foundation.cowin_foudation',
    #                                 related='subproject_id.foundation_id', string=u'基金')
    #
    # the_amount_of_financing = fields.Float(
    #     related='subproject_id.the_amount_of_financing', string=u'本次融资额')
    #
    # the_amount_of_investment = fields.Float(
    #     related='subproject_id.the_amount_of_investment', string=u'本次投资金额')
    # ownership_interest = fields.Integer(
    #     related='subproject_id.ownership_interest', string=u'股份比例')
    # ---------------

    total_assets = fields.Float(string=u'总资产')
    gross_liabilities = fields.Float(string=u'总负债')
    trustee_id = fields.Many2one('hr.employee', string=u'董事')

    compute_round_financing_and_foundation_id = fields.Char(compute=u'_compute_value')

    @api.depends('trustee_id', 'registered_address', 'product')
    def _compute_value(self):
        for rec in self:
            rec.subproject_id.trustee_id = rec.trustee_id
            rec.subproject_id.registered_address = rec.registered_address
            rec.subproject_id.product = rec.product

    accounting_firm = fields.Char(string=u'会计事务所')
    securities_trader = fields.Char(string=u'券商')

    IPOplan = fields.Text(string=u'IPO计划')

    company_status = fields.Text(string=u'公司现状')

    industry_status = fields.Text(string=u'行业现状')




    @api.model
    def create(self, vals):
        tache_info = self._context['tache']

        sub_tache_id = int(tache_info['sub_tache_id'])
        meta_sub_project_id = int(tache_info['meta_sub_project_id'])
        meta_sub_project_entity = self.env['cowin_project.meat_sub_project'].browse(meta_sub_project_id)

        sub_project_id = meta_sub_project_entity.sub_project_ids.id

        target_sub_tache_entity = meta_sub_project_entity.sub_tache_ids.browse(sub_tache_id)

        vals['subproject_id'] = sub_project_id
        res = super(sub_project_annual_analysis_report_on_investment_projects, self).create(vals)

        res._compute_value()  # 写入----> 轮次基金实体
        target_sub_tache_entity.write({
            'res_id': res.id,
            # 'is_unlocked': True,
            'view_or_launch': True,
        })

        # 判断 发起过程 是否需要触发下一个子环节
        # target_sub_tache_entity.check_or_not_next_sub_tache()
        target_sub_tache_entity.update_sub_approval_settings()
        return res

    @api.multi
    def write(self, vals):
        res = super(sub_project_annual_analysis_report_on_investment_projects, self).write(vals)
        tache_info = self._context['tache']

        meta_sub_project_id = int(tache_info['meta_sub_project_id'])

        # 校验meta_sub_project所对应的子工程只能有一份实体
        meta_sub_project_entity = self.env['cowin_project.meat_sub_project'].browse(meta_sub_project_id)

        sub_tache_id = int(tache_info['sub_tache_id'])

        target_sub_tache_entity = meta_sub_project_entity.sub_tache_ids.browse(sub_tache_id)

        target_sub_tache_entity.write({
            'is_launch_again': False,
        })

        # 判断 发起过程 是否需要触发下一个子环节
        # target_sub_tache_entity.check_or_not_next_sub_tache()
        target_sub_tache_entity.update_sub_approval_settings()

        return res

    def load_and_return_action(self, **kwargs):
        tache_info = kwargs['tache_info']
        # tache_info = self._context['tache']
        meta_sub_project_id = int(tache_info['meta_sub_project_id'])

        meta_sub_project_entity = self.env['cowin_project.meat_sub_project'].browse(meta_sub_project_id)

        sub_project_entity = meta_sub_project_entity.sub_project_ids[0]  # 获取子工程实体

        # tem = meta_sub_project_entity.project_id.copy_data()[0]

        res = {}

        common_fileds = [
            'round_financing_id',
            'foundation_id',
            'the_amount_of_financing',
            'the_amount_of_investment',
            'ownership_interest',
        ]

        tem = meta_sub_project_entity.round_financing_and_Foundation_ids[0].read(common_fileds)[0]
        for k, v in tem.iteritems():
            nk = 'default_' + k
            if type(v) is tuple:
                res[nk] = v[0]
            else:
                res[nk] = v

        target_fileds = ['name', 'project_number', 'registered_address', 'production', 'industry', 'founding_time',
                         'stage', 'trustee_id']

        tem = sub_project_entity.read(target_fileds)[0]
        for k, v in tem.iteritems():
            nk = 'default_' + k
            if type(v) is tuple:
                res[nk] = v[0]
            else:
                res[nk] = v

        res['default_investment_phase'] = res['default_stage']
        res['default_reporter'] = self.env.user.employee_ids[0].id
        return {
            'name': self._name,
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'views': [[False, 'form']],
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_id': self.id,
            'target': 'new',
            'context': res,
        }