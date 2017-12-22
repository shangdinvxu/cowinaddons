# -*- coding: utf-8 -*-
from odoo import models, fields, api
import itertools

class Cowin_subprojerct_prcess_tache_status(models.Model):
    _name = 'cowin_project.subproject_process_tache'


    '''
        每个子subproject都有自己的环节状态信息
    '''


    name = fields.Char(string=u'环节名')

    tache_id = fields.Many2one('cowin_project.process_tache', string=u'环节', ondelete="restrict")

    parent_id = fields.Many2one('cowin_project.subproject_process_tache')
    # sub_project_id  = fields.Many2one('cowin_project.cowin_subproject', string=u'字工程名')
    meta_sub_project_id = fields.Many2one('cowin_project.meat_sub_project', string=u'元子工程实例', ondelete="cascade")

    # 这三条数据对应的是不同的子工程的使用,其他数据不会变更
    is_unlocked = fields.Boolean(string=u'是否已解锁', default=False)
    # is_unlocked = fields.Selection([(0, u'未解锁'), (1, u'解锁中'), (2, u'已解锁')], string=u'解锁条件', default=0)
    res_id = fields.Integer(string=u'该环节对应该实例另一个字段model_id中的一个实例')
    view_or_launch = fields.Boolean(string=u'发起或者创建', default=False)


    sub_pro_approval_flow_settings_ids = fields.One2many('cowin_project.sub_approval_flow_settings', 'sub_project_tache_id', string=u'子审批实体')

    order = fields.Integer()

    index = fields.Integer(string=u'多个自定义的环节', default=0)

    # res_id_trigger = fields.Integer(compute='_compute_res_id', store=True)
    #
    # @api.depends('res_id')
    # def _compute_res_id(self):
    #     self.ensure_one()
    #     if self.res_id_trigger > 0:
    #         raise UserWarning(u'只能发起一次请求!!!')
    #
    #     self.res_id_trigger = self.res_id
    #
    #     # 检查提交状态是否有审批节点
    #     if len(self.sub_pro_approval_flow_settings_ids.approval_flow_settings_id.approval_flow_setting_node_ids) == 2:
    #         # 触发下一个环节的激活
    #         self.sub_pro_approval_flow_settings_ids.status = 4
    #
    #         # 触发该字段计算的数据
    #         # self.sub_pro_approval_flow_settings_ids.status_trigger_m()

    def get_tache(self):
        return self.tache_id


    def check_or_not_next_sub_tache(self):
        if self.sub_pro_approval_flow_settings_ids.update_final_approval_flow_settings_status_and_node():
            # 当前子审批实体状态设置为4
            # self.sub_pro_approval_flow_settings_ids.status = 4
            # self.sub_pro_approval_flow_settings_ids.write({
            #         'status': 4,
            #     })

            # self.sub_pro_approval_flow_settings_ids.update_final_approval_flow_settings_status_and_node()
            for sub_tache_entity in self.meta_sub_project_id.sub_tache_ids:

                if sub_tache_entity.parent_id == self:
                                    sub_tache_entity.write({
                                        'is_unlocked': True,
                                        })
                                    break

        else:
            # 调整审核状态

            # 更新子审批实体的状态
            self.sub_pro_approval_flow_settings_ids.update_approval_flow_settings_status_and_node()



    # 重新设定依赖写入的问题
    def set_depency_order_by_sub_tache(self):

        # 找到主工程的环节

        # if len(self) > 1:
        #     this = self[0]

        this = self[0] if len(self) > 1 else self

        base_tache_entity = [tache_entity for tache_entity in this.meta_sub_project_id.project_id.process_id.get_all_tache_entities()
                             if tache_entity.model_id.model_name == this.meta_sub_project_id.project_id._name
                             ][0]


        count = itertools.count(1)
        base_sub_tache_entity = [entity for entity in this.meta_sub_project_id.sub_tache_ids \
                                                            if entity.tache_id.parent_id == base_tache_entity][0]
        base_sub_tache_entity.write({
            'order': count.next(),
        })

        current_sub_tache_entity = base_sub_tache_entity

        a = set()
        while current_sub_tache_entity:
            if current_sub_tache_entity in a:
                break

            for sub_tache_entity in this.meta_sub_project_id.sub_tache_ids:
                if sub_tache_entity == current_sub_tache_entity:
                    a.add(sub_tache_entity)
                    continue
                if sub_tache_entity.parent_id == current_sub_tache_entity:
                    a.add(current_sub_tache_entity)
                    sub_tache_entity.write({'order': count.next()})
                    current_sub_tache_entity = sub_tache_entity



        return 'kk'