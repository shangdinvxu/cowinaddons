# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Cowin_project_subproject_dispatch_report(models.Model):

    '''
        尽调报告
    '''
    _inherit = 'cowin_project.base_status'

    _name = 'cowin_project.subt_dispatch_report'

    subproject_id = fields.Many2one('cowin_project.cowin_subproject', ondelete="cascade")
    sub_tache_id = fields.Many2one('cowin_project.subproject_process_tache', string=u'子环节实体')


    dispatch_report = fields.Many2many('ir.attachment', 'subt_dispatch_report_attachment_rel', string=u'尽调报告')

    attachment_note = fields.Char(string=u'附件说明')


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
        vals['sub_tache_id'] = sub_tache_id
        res = super(Cowin_project_subproject_dispatch_report, self).create(vals)
        target_sub_tache_entity.write({
            'res_id': res.id,
            # 'is_unlocked': True,
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

        return res



    @api.multi
    def write(self, vals):

        # 由于在前端界面中,冲写过前端想后端写入的方法,有空值的影响,所以,我们需要把该问题给过滤掉!!!
        if not vals:
            return True

        res = super(Cowin_project_subproject_dispatch_report, self).write(vals)

        # button在当前的业务逻辑中当前属于审核状态, 分发之后的业务,业务逻辑不同
        if self.button_status == 1 or self.button_status == 2:
            return res
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

        sub_project_entity = meta_sub_project_entity.sub_project_ids[0]  # 获取子工程实体

        # tem = meta_sub_project_entity.project_id.copy_data()[0]

        common_fileds = []

        common_fileds.extend([])


        res = {}

        t_name = self._name + '_form_no_button'
        view_id = self.env.ref(t_name).id

        return {
            'name': self._name,
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