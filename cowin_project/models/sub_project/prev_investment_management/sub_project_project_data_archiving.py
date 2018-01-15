# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
class Cowin_project_subproject_project_data_archiving(models.Model):

    '''
        项目资料归档
    '''
    _inherit = 'cowin_project.base_status'

    _name = 'cowin_project.sub_project_data_archiving'



    subproject_id = fields.Many2one('cowin_project.cowin_subproject', ondelete="cascade")
    sub_tache_id = fields.Many2one('cowin_project.subproject_process_tache', string=u'子环节实体')


    # name = fields.Char(related='subproject_id.name', string=u"项目名称")
    # project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    # invest_manager_id = fields.Many2one('hr.employee', related='subproject_id.invest_manager_id', string=u'投资经理')

    name = fields.Char(string=u"项目名称")
    project_number = fields.Char(string=u'项目编号')
    # invest_manager_id = fields.Many2one('hr.employee', string=u'投资经理')
    invest_manager_ids = fields.Many2many('hr.employee', 'sub_project_data_archiving_invest_manager_employee_rel', string=u'投资经理')


    # engagement_partner_id = fields.Many2one('hr.employee', string=u'项目合伙人')
    engagement_partner_ids = fields.Many2many('hr.employee', 'sub_project_data_archiving_engagement_partner_employee_rel', string=u'项目合伙人')

    # ----------  投资基金
    round_financing_and_foundation_id = fields.Many2one('cowin_project.round_financing_and_foundation',
                                                        related='subproject_id.round_financing_and_foundation_id',
                                                        string=u'基金轮次实体')
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



    investment_decision_process_information = fields.Many2many('ir.attachment', 'investment_decision_process_information_attachment_rel', string=u'投资决策流程资料')
    relevant_legal_documents_and_materials = fields.Many2many('ir.attachment', 'relevant_legal_documents_and_materials_attachment_rel', string=u'相关法律文件资料')
    government_approval_materials = fields.Many2many('ir.attachment', 'government_approval_materials_attachment_rel', string=u'政府审批资料')
    payment_process_information = fields.Many2many('ir.attachment', 'payment_process_information_attachment_rel', string=u'付款流程资料')
    business_change_data = fields.Many2many('ir.attachment', 'business_change_data_attachment_rel', string=u'工商变更资料')

    @api.model
    def create(self, vals):
        tache_info = self._context['tache']

        meta_sub_project_id = int(tache_info['meta_sub_project_id'])

        # 校验meta_sub_project所对应的子工程只能有一份实体
        meta_sub_project_entity = self.env['cowin_project.meat_sub_project'].browse(meta_sub_project_id)
        if len(meta_sub_project_entity.sub_project_ids) > 1:
            raise UserError(u'每个元子工程只能有一份实体!!!')

        sub_tache_id = int(tache_info['sub_tache_id'])

        vals['subproject_id'] = meta_sub_project_entity.sub_project_ids.id
        vals['sub_tache_id'] = sub_tache_id


        target_sub_tache_entity = meta_sub_project_entity.sub_tache_ids.browse(sub_tache_id)

        sub_project = super(Cowin_project_subproject_project_data_archiving, self).create(vals)
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
        res = super(Cowin_project_subproject_project_data_archiving, self).write(vals)
        target_sub_tache_entity = self.sub_tache_id

        if self.inner_or_outer_status == 1:
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


        target_fileds = ['name', 'project_number', 'invest_manager_id']

        tem = sub_project_entity.read(target_fileds)[0]
        for k, v in tem.iteritems():
            nk = 'default_' + k
            if type(v) is tuple:
                res[nk] = v[0]
            else:
                res[nk] = v

        invest_manager_entity = self.env['cowin_common.approval_role'].search([('name', '=', u'投资经理')])
        rel_entities = meta_sub_project_entity.sub_meta_pro_approval_settings_role_rel & invest_manager_entity.sub_meta_pro_approval_settings_role_rel

        res['default_invest_manager_ids'] = [(6, 0, [rel.employee_id.id for rel in rel_entities])]

        engagement_partner_entity = self.env['cowin_common.approval_role'].search([('name', '=', u'项目合伙人')])
        rel_entities = meta_sub_project_entity.sub_meta_pro_approval_settings_role_rel & engagement_partner_entity.sub_meta_pro_approval_settings_role_rel

        res['default_engagement_partner_ids'] = [(6, 0, [rel.employee_id.id for rel in rel_entities])]

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