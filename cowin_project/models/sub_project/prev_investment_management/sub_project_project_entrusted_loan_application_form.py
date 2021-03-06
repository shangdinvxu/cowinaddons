# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
class Cowin_project_subproject_project_entrusted_loan_application_form(models.Model):
    '''
        项目委托贷款申请表
    '''

    _name = 'cowin_project.sub_entrusted_loan_app_form'

    subproject_id = fields.Many2one('cowin_project.cowin_subproject', ondelete="cascade")

    # name = fields.Char(related='subproject_id.name', string=u"项目名称")
    # project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    # invest_manager_id = fields.Many2one('hr.employee', related='subproject_id.invest_manager_id', string=u'投资经理')

    name = fields.Char(string=u"项目名称")
    project_number = fields.Char(string=u'项目编号')
    # invest_manager_id = fields.Many2one('hr.employee', string=u'投资经理')
    invest_manager_ids = fields.Many2many('hr.employee', string=u'投资经理')

    date_of_application = fields.Date(string=u'申请日期')

    # ----------  投资基金

    # round_financing_and_foundation_id = fields.Many2one('cowin_project.round_financing_and_foundation',
    #                                                     related='subproject_id.round_financing_and_foundation_id',
    #                                                     string=u'基金轮次实体')
    round_financing_id = fields.Many2one('cowin_common.round_financing', string=u'融资轮次')
    foundation_id = fields.Many2one('cowin_foundation.cowin_foudation', string=u'基金名称')
    the_amount_of_financing = fields.Float(string=u'本次融资金额')
    the_amount_of_investment = fields.Float(string=u'本次投资金额')
    ownership_interest = fields.Integer(string=u'股份比例')

    # ----------  投资基金
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

    # list_of_examination_and_approval_documents = fields.Many2many('ir.attachment', string=u'审批文件清单')
    list_of_examination_and_approval_documents = fields.Many2many('ir.attachment', 'sub_entrusted_loan_app_form', string=u'审批文件清单')

    time_of_application_for_entrusted_loan = fields.Date(string=u'委托贷款申请时间')
    amount_of_application_for_entrusted_loan = fields.Float(string=u'委托贷款申请金额')
    # amount_of_entrusted_loan = fields.Float(string=u'委托贷款申请金额')

    compute_round_financing_and_foundation_id = fields.Char(compute=u'_compute_value')

    @api.depends('amount_of_application_for_entrusted_loan')
    def _compute_value(self):
        for rec in self:
            rec.subproject_id.amount_of_entrusted_loan = rec.amount_of_application_for_entrusted_loan


    reasons_for_application = fields.Text(string=u'申请原因')
    entrusted_loan_bank = fields.Char(string=u'委托贷款银行')
    lending_rate = fields.Float(string=u'借款利率')
    life_of_loan = fields.Float(string=u'借款期限')
    transfer_charge = fields.Float(string=u'手续费')


    @api.model
    def create(self, vals):
        tache_info = self._context['tache']

        meta_sub_project_id = int(tache_info['meta_sub_project_id'])

        # 校验meta_sub_project所对应的子工程只能有一份实体
        meta_sub_project_entity = self.env['cowin_project.meat_sub_project'].browse(meta_sub_project_id)
        if len(meta_sub_project_entity.sub_project_ids) > 1:
            raise UserError(u'每个元子工程只能有一份实体!!!')

        vals['subproject_id'] = meta_sub_project_entity.sub_project_ids.id

        sub_tache_id = int(tache_info['sub_tache_id'])

        target_sub_tache_entity = meta_sub_project_entity.sub_tache_ids.browse(sub_tache_id)

        sub_project = super(Cowin_project_subproject_project_entrusted_loan_application_form, self).create(vals)
        sub_project._compute_value() # # 写入----> 轮次基金实体
        target_sub_tache_entity.write({
            'res_id': sub_project.id,
            'view_or_launch': True,
        })

        # 判断 发起过程 是否需要触发下一个子环节
        # target_sub_tache_entity.check_or_not_next_sub_tache()
        target_sub_tache_entity.update_sub_approval_settings()

        # 触发下一个依赖子环节处于解锁状态
        # for current_sub_tache_entity in meta_sub_project_entity.sub_tache_ids:
        #     if current_sub_tache_entity.parent_id == target_sub_tache_entity:
        #         current_sub_tache_entity.write({
        #             'is_unlocked': True,
        #         })

        return sub_project

    @api.multi
    def write(self, vals):
        res = super(Cowin_project_subproject_project_entrusted_loan_application_form, self).write(vals)
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

        sub_project_entity = meta_sub_project_entity.sub_project_ids[0] # 获取子工程实体

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


        # target_fileds = ['name', 'project_number', 'invest_manager_id', 'trustee', 'supervisor']
        target_fileds = ['name', 'project_number', 'invest_manager_id', 'amount_of_entrusted_loan']

        tem = sub_project_entity.read(target_fileds)[0]
        for k, v in tem.iteritems():
            nk = 'default_' + k
            if type(v) is tuple:
                res[nk] = v[0]
            else:
                res[nk] = v


        res['default_amount_of_application_for_entrusted_loan'] = res['default_amount_of_entrusted_loan']

        # 默认的投资经理的数据我们需要去自定义添加
        invest_manager_entity = self.env['cowin_common.approval_role'].search([('name', '=', u'投资经理')])
        rel_entities = meta_sub_project_entity.sub_meta_pro_approval_settings_role_rel & invest_manager_entity.sub_meta_pro_approval_settings_role_rel

        res['default_invest_manager_ids'] = [(6, 0, [rel.employee_id.id for rel in rel_entities])]

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

