# -*- coding: utf-8 -*-
from odoo import models, fields, api

class sub_project_quarterly_analysis_report_on_investment_projects(models.Model):
    _inherit = 'cowin_project.base_status'


    _name = 'cowin_project.sub_quarterly_analysis_report'


    '''
        投资项目季度分析报告

    '''

    # 用于显示环节中的名称
    _rec_name = 'sub_tache_id'

    subproject_id = fields.Many2one('cowin_project.cowin_subproject', ondelete="cascade")
    sub_tache_id = fields.Many2one('cowin_project.subproject_process_tache', string=u'子环节实体')


    # name = fields.Char(related='subproject_id.name', string=u"项目名称")
    # project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')

    name = fields.Char(string=u"项目名称")
    project_number = fields.Char(string=u'项目编号')

    reporter = fields.Many2one('hr.employee', string=u'报告人')

    filing_date = fields.Date(string=u'提交日期', default=fields.Date.today())
    # compute字段
    compute_filing_date = fields.Char(string=u'根据重新发起来计算申请日期', compute='_compute_filing_date')

    def _compute_filing_date(self):
        if self.sub_tache_id.is_launch_again:
            self.write({
                'filing_date': fields.Date.today(),
            })

    registered_address = fields.Char(string=u'注册地')

    chairman = fields.Char(string=u'董事长')

    general_manager = fields.Char(string=u'总经理')

    production = fields.Text(string=u'产品')

    industry = fields.Many2one('cowin_common.cowin_industry', string=u'所属行业')

    founding_time = fields.Date(string=u'成立时间')

    investment_phase = fields.Selection([(1, u'种子期'), (2, u'成长早期'), (3, u'成长期'), (4, u'成熟期')], string=u'投资阶段', default=1)
    current_phase = fields.Selection([(0, u'种子期'), (1, u'成长早期'), (2, u'成长期'), (3, u'成熟期')], string=u'当前阶段')

    # ----------  投资基金
    round_financing_and_foundation_id = fields.Many2one('cowin_project.round_financing_and_foundation',
                                                        related='subproject_id.round_financing_and_foundation_id',
                                                        string=u'基金轮次实体')
    round_financing_id = fields.Many2one('cowin_common.round_financing', string=u'融资轮次')
    foundation_id = fields.Many2one('cowin_foundation.cowin_foundation', string=u'基金名称')
    the_amount_of_financing = fields.Float(string=u'本次融资金额')
    the_amount_of_investment = fields.Float(string=u'本次投资金额')
    ownership_interest = fields.Float(string=u'股份比例')
    project_valuation = fields.Float(string=u'估值')


    total_assets = fields.Float(string=u'总资产')
    gross_liabilities = fields.Float(string=u'总负债')
    trustee_id = fields.Many2one('hr.employee', string=u'董事')


    compute_round_financing_and_foundation_id = fields.Char(compute=u'_compute_value')

    # @api.depends('trustee_id', 'registered_address', 'product')
    # def _compute_value(self):
    #     for rec in self:
    #         rec.subproject_id.trustee_id = rec.trustee_id
    #         rec.subproject_id.registered_address = rec.registered_address
    #         rec.subproject_id.product = rec.product

    accounting_firm = fields.Char(string=u'会计事务所')
    securities_trader = fields.Char(string=u'券商')


    IPOplan = fields.Text(string=u'IPO计划')

    company_status = fields.Text(string=u'公司现状')

    industry_status = fields.Text(string=u'行业现状')

    # 审批实体记录
    sub_pro_approval_flow_settings_record_ids = fields.One2many('cowin_project.sub_approval_flow_settings_record',
                                                                'res_id', string=u'审批记录',
                                                                domain=lambda self: [('res_model', '=', self._name)])



    @api.multi
    def write_date_of_review_to_related_model(self):
        for rec in self:
            rec.subproject_id.trustee_id = rec.trustee_id
            rec.subproject_id.registered_address = rec.registered_address
            rec.subproject_id.production = rec.production


    @api.model
    def create(self, vals):
        tache_info = self._context['tache']

        sub_tache_id = int(tache_info['sub_tache_id'])
        meta_sub_project_id = int(tache_info['meta_sub_project_id'])
        meta_sub_project_entity = self.env['cowin_project.meat_sub_project'].browse(meta_sub_project_id)

        sub_project_id = meta_sub_project_entity.sub_project_ids.id

        target_sub_tache_entity = meta_sub_project_entity.sub_tache_ids.browse(sub_tache_id)

        vals['subproject_id'] = sub_project_id
        vals['sub_tache_id'] = sub_tache_id

        res = super(sub_project_quarterly_analysis_report_on_investment_projects, self).create(vals)
        res.write_date_of_review_to_related_model() # 写入----> 轮次基金实体
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
        # 重新发起的操作!!!需要鉴别数据
        target_sub_tache_entity = self.sub_tache_id
        if self._context.get('is_launch_again'):
            target_sub_tache_entity.write({
                'is_launch_again': False,
            })

            # 重新发起状态,需要重新写入相关的数据
            self.write_date_of_review_to_related_model()

            # 判断 发起过程 是否需要触发下一个子环节

            target_sub_tache_entity.update_sub_approval_settings()

        # 由于在前端界面中,重写过前端想后端写入的方法,有空值的影响, 尤其是button的操作的影响,所以,我们需要把该问题给过滤掉!!!
        if not vals:
            return True

        # self.write_date_of_review_to_related_model()
        res = super(sub_project_quarterly_analysis_report_on_investment_projects, self).write(vals)

        return res



    def load_and_return_action(self, **kwargs):
        tache_info = kwargs['tache_info']
        # tache_info = self._context['tache']
        meta_sub_project_id = int(tache_info['meta_sub_project_id'])

        meta_sub_project_entity = self.env['cowin_project.meat_sub_project'].browse(meta_sub_project_id)

        sub_project_entity = meta_sub_project_entity.sub_project_ids[0] # 获取子工程实体

        # tem = meta_sub_project_entity.project_id.copy_data()[0]

        res = {}


        common_fileds = [
            'round_financing_id',
            'foundation_id',
            'the_amount_of_financing',
            'the_amount_of_investment',
            'ownership_interest',
            'project_valuation',
        ]

        tem = meta_sub_project_entity.round_financing_and_Foundation_ids[0].read(common_fileds)[0]
        for k, v in tem.iteritems():
            nk = 'default_' + k
            if type(v) is tuple:
                res[nk] = v[0]
            else:
                res[nk] = v


        target_fileds = ['name', 'project_number', 'registered_address', 'production', 'industry', 'founding_time', 'stage', 'trustee_id']

        tem = sub_project_entity.read(target_fileds)[0]
        for k, v in tem.iteritems():
            nk = 'default_' + k
            if type(v) is tuple:
                res[nk] = v[0]
            else:
                res[nk] = v

        res['default_investment_phase'] = res['default_stage']

        res['default_reporter'] = self.env.user.employee_ids[0].id

        t_name = self._name + '_form_no_button'
        view_id = self.env.ref(t_name).id

        return {
            'name': tache_info['name'],
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'views': [[view_id, 'form']],
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_id': self.id,
            'target': 'new',
            'context': res,
        }