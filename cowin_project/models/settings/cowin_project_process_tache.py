# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class Cowin_project_process_tache(models.Model):
    _name = 'cowin_project.process_tache'

    name = fields.Char(string=u'环节')
    parent_id = fields.Many2one('cowin_project.process_tache', string=u'解锁条件')

    tache_status_id = fields.One2many('cowin_project.subproject_process_tache', 'tache_id', '各个子工程的环节配置信息')

    description = fields.Char(string=u'说明')
    state = fields.Boolean(string=u'启用状态', default=True)

    is_unlocked = fields.Boolean(string=u'是否已解锁', default=False)

    stage_id = fields.Many2one('cowin_project.process_stage', ondelete="cascade")
    # process_id=fields.Many2one('cowin_settings.process', related='stage_id.process_id')

    once_or_more = fields.Boolean(string=u'发起次数', default=False)
    view_or_launch = fields.Boolean(string=u'发起或者新增', default=False)

    model_id = fields.Many2one(u'cowin_settings.custome_model_data', string=u'自定义model的名字')


    # 这种情况只适用于主project的使用,子project只适用于环节的下一级表
    res_id = fields.Integer(string=u'该环节对应该实例另一个字段model_id中的一个实例')
    # 这种情况只适用于主project的使用,子project只适用于环节的下一级表
    approval_flow_settings_ids = fields.One2many('cowin_project.approval_flow_settings', 'tache_id', string=u'审批流程')


    @api.model
    def create(self, vals):

        res = super(Cowin_project_process_tache, self).create(vals)

        # 创建的过程中开始创建审批流实体
        approval_flow_settings = self.env['cowin_project.approval_flow_settings'].create({
            'tache_id': res.id,
        })

        return res

    def _check_parent_id(self, ids=[]):

        # 如果parent_id为空的情况下,到达了顶层
        if not self.parent_id.id:
            return True

        # 如果parent_id不为空的, 相互引用的话,直接返回为False
        # 不过,这里情况可以包含在抽象递归调用之中
        # if self.id == self.parent_id.id:
        #     return False

        # 如果便利的节点的列表为空的情况下,直接返回True
        # if not ids:
        #     return True

        if self.id in ids:
            return False

        ids.append(self.id)

        return self.parent_id._check_parent_id(ids)



    # 检查依赖的记录之间时候会有环的形成!!1
    def on_set_parent_id(self):
        ids = []
        print u'kkkk'
        return self._check_parent_id(ids)



    def get_approval_flow_settings(self):
        res = None
        if not self.approval_flow_settings:
            res = self.env['cowin_project.approval_flow_settings'].create({'name': u'审批流'})
            res.tache_id = self

        else:
            res = self.approval_flow_settings
        return res


    def create_tache_info(self, tache_info, stage_id):

        model_name = self.env['cowin_settings.custome_model_data'].search([('model_name', '=', tache_info['model_name'])])



        # 弄人情况下在环节中已经创建好审批流实体
        tache_entity = self.create({
            'name': tache_info['name'],
            'description': tache_info['description'],
            'state': tache_info['state'],
            'once_or_more': tache_info['once_or_more'],
            'model_id': model_name.id,
            'stage_id': stage_id,
            # 'approval_flow_settings_id': tache_info['approval_flow_settings_id'],
        })


        # 构建审批流

        approval_flow_settings_entity = tache_entity.approval_flow_settings_ids

        approval_flow_settings_id = int(tache_info['approval_flow_settings_id'])

        meta_approval_flow_settings_entity = self.env['cowin_settings.approval_flow_settings'].browse(approval_flow_settings_id)

        meta_approval_flow_settings_node_entities = meta_approval_flow_settings_entity.approval_flow_setting_node_ids

        for meta_node in meta_approval_flow_settings_node_entities:
            target_node = self.env['cowin_project.approval_flow_setting_node'].create({
                'name': meta_node.name,
                'active_withdrawal': meta_node.active_withdrawal,
                'approval_flow_settings_id': approval_flow_settings_entity.id,
            })

            # 把之前需要元配置中审批节点实体中的Many2Many所在的权限角色实体,全部都复制在主工程中的权限决策实体中
            cowin_project_node_approval_operation_role_rel = self.env['cowin_project_node_approval_operation_role_rel']

            for operation_role in meta_node.operation_role_ids:
                cowin_project_node_approval_operation_role_rel.create({
                    'approval_flow_setting_node_id': target_node.id,
                    'operation_role_id': operation_role.id,
                })




