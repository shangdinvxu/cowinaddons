# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Cowin_sub_project_approval_flow_settings(models.Model):
    _name = 'cowin_project.sub_approval_flow_settings'

    '''
        每个子工程都会有自己的审批流的,所以需要保存属于自己的审批流程的节点的信息
    '''


    name = fields.Char(string=u'子工程审批流节点信息')

    # tache_id = fields.Many2one('cowin_project.process_tache', string=u'环节')
    approval_flow_settings_id = fields.Many2one('cowin_project.approval_flow_settings', string=u'工程审批流')
    meta_sub_project_id = fields.Many2one('cowin_project.meat_sub_project', string=u'元子工程实例')


    # 用以记录当前的审批节点的位置

    approval_flow_node_id = fields.Many2one('cowin_project.approval_flow_setting_node', string=u'当前的审批节点所在的位置!!!')






