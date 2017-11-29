# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Cowin_project_approval_flow_settings(models.Model):
    _name = 'cowin_project.approval_flow_settings'

    name = fields.Char(string=u'审批流名称')

    tache_id = fields.Many2one('cowin_project.process_tache', string=u'依赖环节')

    approval_flow_setting_node_ids = fields.One2many('cowin_project.approval_flow_setting_node', 'approval_flow_settings_id', u'审批节点')

    _sql_constraints = [
        ('login_key', 'UNIQUE (name)', u'审批配置名称不能相同!!!')
    ]


    def get_all_approval_flow_setting_nodes(self):
        res = []
        for node in self.approval_flow_setting_node_ids:
            tmp = {}
            tmp['approval_flow_setting_node_id'] = node.id
            tmp['name'] = node.name
            tmp['approval_flow_settings_id'] = node.approval_flow_settings_id.id

            res.append(tmp)

        return res

    @api.model
    def create(self, vals):
        res = super(Cowin_project_approval_flow_settings, self).create(vals)
        return res


    # 因为这里面内部的节点基本上是复制元审批节点的信息,所以不必要再次去产生默认的节点的信息
    def create_approval_flow_settings_entity(self, approval_flow_nodes_info, tache_id):
        res = self.create({
            'tache_id': tache_id,
        })

        approval_flow_nodes_info = approval_flow_nodes_info['approval_flow_nodes_info']
        node_entities = []
        for node_info in approval_flow_nodes_info:
            node = res.approval_flow_setting_node_ids.create({
                'approval_flow_settings_id': res.id,
                'name': node_info['operation_role_id'],
                'order': node_info['order'],
                'accept': node_info['accept'],
                'reject': node_info['reject'],
                'put_off': node_info['put_off'],
            })

            node_entities.append(node)


        # 修复依赖的节点的关系

        node_entities = sorted(node_entities, key=lambda node_entity: node_entity.order)

        for i, node_entity in enumerate(node_entities[:-1]):
            node_entity.write({
                'parent_id': node_entities[i+1].id,
            })






class Cowin_project_approval_role_inherit(models.Model):


    _inherit = 'cowin_common.approval_role'


    approval_flow_setting_node_ids = fields.One2many('cowin_project.approval_flow_setting_node','operation_role_id',
                                                     string=u'审批节点')



class Cowin_project_approval_flow_setting_node(models.Model):
    _name = 'cowin_project.approval_flow_setting_node'

    name = fields.Char(string=u'审批节点')

    approval_flow_settings_id = fields.Many2one('cowin_project.approval_flow_settings', string=u'审批流',
                                                ondelete="cascade")

    operation_role_id = fields.Many2one('cowin_common.approval_role', string=u'操作角色')

    active_withdrawal = fields.Boolean(string=u'主动撤回')

    _sql_constraints = [
        ('name_key', 'UNIQUE (approval_flow_settings_id, name)', u'审批节点名称不能相同!!!'),
    ]




