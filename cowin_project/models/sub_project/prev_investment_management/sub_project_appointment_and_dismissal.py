# -*- coding: utf-8 -*-
from odoo import models, fields, api
class Cowin_project_subproject_appointment_and_dismissal(models.Model):

    '''

        董事／监事任免书
    '''

    _name = 'cowin_project.sub_appointment_and_dismissal'

    subproject_id = fields.Many2one('cowin_project.cowin_subproject', ondelete="cascade")

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    invest_manager_id = fields.Many2one('hr.employee', related='subproject_id.invest_manager_id', string=u'投资经理')

    #----- 任免对象
    trustee_id = fields.Many2one('hr.employee', string=u'董事')
    appointment_time_begin_trustee = fields.Date(string=u'开始日期')
    appointment_time_end_trustee = fields.Date(string=u'结束日期')

    Tenure_trustee = fields.Float(string=u'任职年限')

    supervisor_id = fields.Many2one('hr.employee', string=u'监事')
    appointment_time_begin_supervisor = fields.Date(string=u'开始日期')
    appointment_time_endr_supervisor = fields.Date(string=u'结束日期')

    Tenure_supervisor = fields.Float(string=u'任职年限')


    compute_round_financing_and_foundation_id = fields.Char(compute=u'_compute_value')

    @api.depends('supervisor_id', 'trustee_id')
    def _compute_value(self):
        for rec in self:
            rec.subproject_id.trustee_id = rec.trustee_id
            rec.subproject_id.supervisor_id = rec.supervisor_id




    #------

    managing_partner_ids = fields.Many2many('hr.employee', string=u'管理合伙人')

    @api.model
    def create(self, vals):
        tache_info = self._context['tache']

        # sub_project_id = int(tache_info['sub_project_id'])

        sub_tache_id = int(tache_info['sub_tache_id'])
        meta_sub_project_id = int(tache_info['meta_sub_project_id'])
        meta_sub_project_entity = self.env['cowin_project.meat_sub_project'].browse(meta_sub_project_id)

        sub_project_id = meta_sub_project_entity.sub_project_ids.id

        target_sub_tache_entity = meta_sub_project_entity.sub_tache_ids.browse(sub_tache_id)

        vals['subproject_id'] = sub_project_id
        res = super(Cowin_project_subproject_appointment_and_dismissal, self).create(vals)

        res._compute_value() # 写入----> 轮次基金实体


        target_sub_tache_entity.write({
            'res_id': res.id,
            # 'is_unlocked': True,
            'view_or_launch': True,
        })

        # 判断 发起过程 是否需要触发下一个子环节
        # target_sub_tache_entity.check_or_not_next_sub_tache()
        target_sub_tache_entity.update_sub_approval_settings()

        # # 触发下一个依赖子环节处于解锁状态
        # for current_sub_tache_entity in meta_sub_project_entity.sub_tache_ids:
        #     if current_sub_tache_entity.parent_id == target_sub_tache_entity:
        #         current_sub_tache_entity.write({
        #             'is_unlocked': True,
        #         })

        return res



    @api.multi
    def write(self, vals):
        res = super(Cowin_project_subproject_appointment_and_dismissal, self).write(vals)
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


        target_fileds = ['name', 'project_number', 'invest_manager_id', 'supervisor_id', 'trustee_id']

        tem = sub_project_entity.read(target_fileds)[0]
        for k, v in tem.iteritems():
            nk = 'default_' + k
            if type(v) is tuple:
                res[nk] = v[0]
            else:
                res[nk] = v

        # 默认的投资经理的数据我们需要去自定义添加
        invest_manager_entity = self.env['cowin_common.approval_role'].search([('name', '=', u'投资经理')])
        rel_entities = meta_sub_project_entity.sub_meta_pro_approval_settings_role_rel & invest_manager_entity.sub_meta_pro_approval_settings_role_rel

        res['default_invest_manager_ids'] = [(6, 0, [rel.employee_id.id for rel in rel_entities])]

        investment_decision_committee_entity = self.env['cowin_common.approval_role'].search(
            [('name', '=', u'投资决策委员')])
        rel_entities = meta_sub_project_entity.sub_meta_pro_approval_settings_role_rel & investment_decision_committee_entity.sub_meta_pro_approval_settings_role_rel
        res['default_investment_decision_committee_ids'] = [(6, 0, [rel.employee_id.id for rel in rel_entities])]

        managing_partner_ids_entity = self.env['cowin_common.approval_role'].search([('name', '=', u'管理合伙人')])
        rel_entities = meta_sub_project_entity.sub_meta_pro_approval_settings_role_rel & managing_partner_ids_entity.sub_meta_pro_approval_settings_role_rel

        res['default_managing_partner_ids'] = [(6, 0, [rel.employee_id.id for rel in rel_entities])]

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
