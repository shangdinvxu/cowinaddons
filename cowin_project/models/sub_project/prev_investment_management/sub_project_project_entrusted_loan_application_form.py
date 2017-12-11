# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
class Cowin_project_subproject_project_entrusted_loan_application_form(models.Model):
    '''
        项目委托贷款申请表
    '''

    _name = 'cowin_project.sub_entrusted_loan_app_form'

    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    invest_manager_id = fields.Many2one('hr.employee', related='subproject_id.invest_manager_id', string=u'投资经理')

    date_of_application = fields.Date(string=u'申请日期')

    # ----------  投资基金
    round_financing_id = fields.Many2one('cowin_common.round_financing',
                                         related='subproject_id.round_financing_id', string=u'轮次')

    foundation_id = fields.Many2one('cowin_foundation.cowin_foudation',
                                    related='subproject_id.foundation_id', string=u'基金')

    the_amount_of_financing = fields.Float(
        related='subproject_id.the_amount_of_financing', string=u'本次融资额')

    the_amount_of_investment = fields.Float(
        related='subproject_id.the_amount_of_investment', string=u'本次投资金额')
    ownership_interest = fields.Integer(
        related='subproject_id.ownership_interest', string=u'股份比例')
    # ---------------

    list_of_examination_and_approval_documents = fields.Many2many('ir.attachment', string=u'审批文件清单')

    time_of_application_for_entrusted_loan = fields.Date(string=u'委托贷款申请时间')
    amount_of_application_for_entrusted_loan = fields.Float(string=u'委托贷款申请金额')
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

        vals['meta_sub_project_id'] = meta_sub_project_id

        sub_tache_id = int(tache_info['sub_tache_id'])

        target_sub_tache_entity = meta_sub_project_entity.sub_tache_ids.browse(sub_tache_id)

        sub_project = super(Cowin_project_subproject_project_entrusted_loan_application_form, self).create(vals)
        target_sub_tache_entity.write({
            'res_id': sub_project.id,
            'view_or_launch': True,
        })

        # 触发下一个依赖子环节处于解锁状态
        # for current_sub_tache_entity in meta_sub_project_entity.sub_tache_ids:
        #     if current_sub_tache_entity.parent_id == target_sub_tache_entity:
        #         current_sub_tache_entity.write({
        #             'is_unlocked': True,
        #         })

        return sub_project



