# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class Cowin_settings_approval_flow_settings(models.Model):
    _name = 'cowin_settings.approval_flow_settings'

    name = fields.Char(string=u'审批流名称')

    # operational_role_ids = fields.Many2many('hr.employee', string=u'操作角色')

    # active_withdrawal = fields.Boolean(string=u'主动撤回', default=True)

    tache_id = fields.Many2one('cowin_settings.process_tache', string=u'依赖环节', ondelete="cascade")

    approval_flow_settings_node_ids = fields.One2many('cowin_settings.approval_flow_setting_node',
                                                                    'approval_flow_settings_id', u'审批节点')

    _sql_constraints = [
        ('name_key', 'UNIQUE (name)', u'审批配置名称不能相同!!!')
    ]


    def get_all_approval_flow_setting_nodes(self):
        operator_roles = self.env['cowin_common.approval_role'].search([])

        res = []
        for node in self.approval_flow_settings_node_ids:
            tmp = {}
            tmp['approval_flow_setting_node_id'] = node.id
            tmp['name'] = node.name
            tmp['approval_flow_settings_id'] = node.approval_flow_settings_id.id
            tmp['accept'] = node.accept
            tmp['reject'] = node.reject
            tmp['put_off'] = node.put_off
            tmp['operator_roles'] = [operator_role.id for operator_role in node.operation_role_ids]
            tmp['all_operator_roles'] = [operator_role.id for operator_role in operator_roles]

            res.append(tmp)

        return res


    @api.model
    def create(self, vals):

        '''
            目的在于,有默认的操作需要去实现操作的类型!!!
        :param vals:
        :return:
        '''
        res = super(Cowin_settings_approval_flow_settings, self).create(vals)

        self.env['cowin_settings.approval_flow_setting_node'].create({
            'approval_flow_settings_id': res.id,
            'name': u'提交',
        })

        self.env['cowin_settings.approval_flow_setting_node'].create({
            'approval_flow_settings_id': res.id,
            'name': u'审批结束',
        })

        return res



class Cowin_settings_approval_role_inherit(models.Model):

    # _name = 'cowin_settings.approval_role'

    _inherit = 'cowin_common.approval_role'

    approval_flow_setting_node_ids = fields.Many2many('cowin_settings.approval_flow_setting_node', 'cowin_settings_node_approval_operation_role_rel',
                            'operation_role_id' , 'approval_flow_setting_node_id', string=u'操作角色')




class Cowin_approval_flow_setting_node(models.Model):
    _name = 'cowin_settings.approval_flow_setting_node'

    name = fields.Char(string=u'审批节点')

    approval_flow_settings_id = fields.Many2one('cowin_settings.approval_flow_settings', string=u'审批流', ondelete="cascade")


    operation_role_ids = fields.Many2many('cowin_common.approval_role', 'cowin_settings_node_approval_operation_role_rel',
                                          'approval_flow_setting_node_id', 'operation_role_id', string=u'操作角色')

    accept = fields.Boolean(string=u'同意', default=True)
    reject = fields.Boolean(string=u'不同意', default=True)
    put_off = fields.Boolean(string=u'暂缓', default=False)

    _sql_constraints = [
        ('name_key', 'UNIQUE (approval_flow_settings_id, name)', u'审批节点名称不能相同!!!'),
    ]



    @api.model
    def create(self, vals):
        # 把特殊情况屏蔽过去
        res = super(Cowin_approval_flow_setting_node, self).create(vals)

        if vals['name'] != u'提交':
            if len(res.operation_role_ids) > 1:
                raise UserError(u'除了提交节点外,其他节点都只能有一个操作角色!!!')

        return res


    @api.multi
    def write(self, vals):

        res = super(Cowin_approval_flow_setting_node, self).write(vals)
        if vals['name'] != u'提交':
            if len(res.operation_role_ids) > 1:
                raise UserError(u'除了提交节点外,其他节点都只能有一个操作角色!!!')

        return res


