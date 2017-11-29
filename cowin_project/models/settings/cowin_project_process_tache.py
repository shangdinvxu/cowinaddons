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
        # 理论上只会由一条就记录
        return self.approval_flow_settings_ids

    # # 内部调用的方法
    # # 创建审批流实体
    # def _create_approval_flow_settings_entity(self):
    #     # 创建的过程中开始创建审批流实体,这部的操作构建在普通的方法之中
    #     approval_flow_settings = self.env['cowin_project.approval_flow_settings'].create({
    #         'tache_id': self.id,
    #     })



    def create_tache_info(self, tache_info, stage_id):

        # 在新创建环节的情况下mode_id也是空的
        model_entity = self.model_id.search([('model_name', '=', tache_info['model_name'])])



        # 通过外部调用创建工程环节实体
        tache_entity = self.create({
            'name': tache_info['name'],
            'description': tache_info['description'],
            'state': tache_info['state'],
            'once_or_more': tache_info['once_or_more'],
            'model_id': model_entity.id,
            'stage_id': stage_id,
        })

        approval_flow_settings_info = tache_info['approval_flow_settings_info']

        for approval_flow_setting_info in approval_flow_settings_info:
            tache_entity.approval_flow_settings_ids.create_approval_flow_settings_entity(
                approval_flow_setting_info, tache_entity.id)

