# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Cowin_approval_flow_settings(models.Model):
    _name = 'cowin_settings.approval_flow_settings'

    name = fields.Char(string=u'审批流')

    operational_role = fields.Many2many('hr.employee', string=u'操作角色')

    active_withdrawal = fields.Boolean(string=u'主动撤回', default=True)

    tache_id = fields.Many2one('cowin_settings.process_tache', string=u'依赖环节')

    approval_flow_setting_nodes = fields.One2many('cowin_settings.approval_flow_setting_node', 'approval_flow_settings_id', u'审批节点')


    def get_all_approval_flow_setting_nodes(self):
        res = []
        for node in self.approval_flow_setting_nodes:
            tmp = {}
            tmp['approval_flow_setting_node_id'] = node.id
            tmp['name'] = node.name
            tmp['approval_flow_settings_id'] = node.approval_flow_settings_id.id

            res.append(tmp)

        return res


class Cowin_approval_flow_setting_node(models.Model):
    _name = 'cowin_settings.approval_flow_setting_node'

    name = fields.Char(string=u'审批节点')

    approval_flow_settings_id = fields.Many2one('cowin_settings.approval_flow_settings', string=u'审批流')


    # next_node = fields.Many2one


