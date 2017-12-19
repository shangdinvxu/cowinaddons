# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import itertools

class Cowin_settings_approval_flow_settings(models.Model):
    _name = 'cowin_settings.approval_flow_settings'

    name = fields.Char(string=u'审批流名称')


    tache_id = fields.Many2one('cowin_settings.process_tache', string=u'依赖环节', ondelete="cascade")

    approval_flow_settings_node_ids = fields.One2many('cowin_settings.approval_flow_setting_node',
                                                                    'approval_flow_settings_id', u'审批节点')

    _sql_constraints = [
        ('name_key', 'UNIQUE (name)', u'审批配置名称不能相同!!!')
    ]



    # 前端获取的审批流与审批节点的数据
    def get_all_approval_flow_setting_nodes(self):
        operator_roles = self.env['cowin_common.approval_role'].search([])


        # 由于前台需要排序,所以这个地方使用了排序的策略
        # approval_flow_settings_node_ids = self.env['cowin_settings.approval_flow_setting_node'].search(
        #     [('approval_flow_settings_id', '=', self.id)], order='order')
        approval_flow_settings_node_ids = self.approval_flow_settings_node_ids.sorted('order')

        res = []
        for node in approval_flow_settings_node_ids:
            tmp = {}
            tmp['approval_flow_setting_node_id'] = node.id
            tmp['name'] = node.name
            tmp['approval_flow_settings_id'] = node.approval_flow_settings_id.id
            tmp['accept'] = node.accept
            tmp['reject'] = node.reject
            tmp['put_off'] = node.put_off
            tmp['order'] = node.order
            tmp['parent_id'] = node.parent_id.id
            tmp['operation_role_id'] = node.operation_role_id.id
            tmp['all_operator_role_ids'] = [{'operator_role_id': operator_role.id, 'name': operator_role.name}
                                         for operator_role in operator_roles]

            res.append(tmp)
        return res



    # 前端返回数据,可能有添加节点,也可能是删除节点,但也可能是修改节点中内容的信息
    def save_all_approval_flow_setting_nodes(self, approval_flow_setting_nodes_info):
        # approval_flow_setting_nodes_info = kwargs.get('approval_flow_setting_nodes')

        create_nodes = [node for node in approval_flow_setting_nodes_info if node['approval_flow_setting_node_id'] == -1]

        remaings_node_ids = set(node['approval_flow_setting_node_id'] for node in approval_flow_setting_nodes_info
                                            if node['approval_flow_setting_node_id'] != -1)

        origin_node_ids = set(node.id for node in self.approval_flow_settings_node_ids)

        unlink_node_ids = origin_node_ids - remaings_node_ids

        # 删除节点
        for id in unlink_node_ids:
            node = self.env['cowin_settings.approval_flow_setting_node'].browse(id)
            node.unlink()


        # 编辑节点
        remaings_nodes = [node for node in approval_flow_setting_nodes_info if node['approval_flow_setting_node_id'] != -1]
        for node_info in remaings_nodes:
            node = self.env['cowin_settings.approval_flow_setting_node'].browse(node_info['approval_flow_setting_node_id'])
            # role_ids = node_info['operation_role_ids']
            node.write({
                'name': node_info['name'],
                'accept': node_info['accept'],
                'reject': node_info['reject'],
                'put_off': node_info['put_off'],
                # 'operation_role_ids': [(6, 0, role_ids)],
                'operation_role_id': node_info['operation_role_id'],
            })



        #  创建节点
        for node in create_nodes:
            # create a new node!!!
            # role_ids = node['operation_role_ids']
            # self.env['cowin_settings.approval_flow_setting_node'].create({
            approval_flow_setting_node_entity = self.approval_flow_settings_node_ids.create({
                'name': node['name'],
                'approval_flow_settings_id': self.id,
                'accept': node['accept'],
                'reject': node['reject'],
                'put_off': node['put_off'],
                # 'operation_role_ids': [(6, 0, role_ids)],
                # 'operation_role_id': node['operation_role_id'],
            })

            # 通过写入的方法把审批节点写入进去!!!
            approval_flow_setting_node_entity.write({'operation_role_id': node['operation_role_id']})






        return {'result': 'success'}





    @api.model
    def create(self, vals):

        '''
            目的在于,有默认的操作需要去实现操作的类型!!!
        :param vals:
        :return:
        '''
        res = super(Cowin_settings_approval_flow_settings, self).create(vals)



        parent = self.approval_flow_settings_node_ids.create({
            'approval_flow_settings_id': res.id,
            'name': u'审批结束',
            'order': 2,
        })

        self.approval_flow_settings_node_ids.create({
            'approval_flow_settings_id': res.id,
            'name': u'提交',
            'parent_id': parent.id,
            'order': 1,
        })

        return res


#
class Cowin_settings_approval_role_inherit(models.Model):

    _inherit = 'cowin_common.approval_role'
#
#
    #
    approval_flow_setting_node_ids = fields.One2many('cowin_settings.approval_flow_setting_node',
                                                   'operation_role_id'  , string=u'审批节点')




class Cowin_approval_flow_setting_node(models.Model):
    _name = 'cowin_settings.approval_flow_setting_node'

    name = fields.Char(string=u'审批节点')

    approval_flow_settings_id = fields.Many2one('cowin_settings.approval_flow_settings', string=u'审批流', ondelete="cascade")

    parent_id = fields.Many2one('cowin_settings.approval_flow_setting_node', string=u'依赖的父node')


    operation_role_id = fields.Many2one('cowin_common.approval_role', string=u'操作角色', ondelete="restrict")

    order = fields.Integer(string=u'对于前端来说需要排序的字段')

    accept = fields.Boolean(string=u'同意', default=True)
    reject = fields.Boolean(string=u'不同意', default=True)
    put_off = fields.Boolean(string=u'暂缓', default=False)

    _sql_constraints = [
        ('name_key', 'UNIQUE (approval_flow_settings_id, name)', u'审批节点名称不能相同!!!'),
    ]



    @api.model
    def create(self, vals):
        # 默认情况下,给每个审批节点添加一个默认的审批角色
        that = self if len(self) <= 1 else self[0]
        operation_role_entity = that.operation_role_id.search([])[0]
        vals['operation_role_id'] = operation_role_entity.id
        res = super(Cowin_approval_flow_setting_node, self).create(vals)
        res._fix_dependency_at_create()
        return res



    # 前端显示,需要考虑到审批节点依赖的问题!!!
    def _fix_dependency_at_create(self):

        # 必须考虑到其他节点不能包含 '提交' , '审批结束' 这两个节点
        if self.name == u'提交' or self.name == u'审批结束':
            return

        # 拿出审批流节点数据开始进行依赖引用操作
        # nodes = self.env[self._name].search([('approval_flow_settings_id', '=', self.approval_flow_settings_id.id)])

        # 获得该审批节点属于的审批流的所有的节点,包括自己
        nodes = self.approval_flow_settings_id.approval_flow_settings_node_ids
        begin_node = None

        # 需要找到初始化提交的节点
        for node in nodes:
            if node.name == u'提交':
                begin_node = node
                break

        current_node = begin_node

        if current_node:

            while current_node.parent_id.name != u'审批结束':
                current_node = current_node.parent_id

            # 在最后节点的之前添加新的节点
            end_node = current_node.parent_id

            self.write({
                'parent_id': end_node.id,
            })

            current_node.write({
                'parent_id': self.id,
            })

            # 计数生成器
            counter = itertools.count(1, 1)

            current_node = begin_node

            while current_node:
                current_node.write({
                    'order': counter.next(),
                })

                current_node = current_node.parent_id

    # 前端显示,需要考虑到审批节点依赖的问题!!!
    def _fix_dependency_at_unlink(self):

        # 必须考虑到其他节点不能包含 '提交' , '审批结束' 节点
        if self.name == u'提交' or self.name == u'审批结束':
            return

        # 拿出节点数据开始进行依赖引用操作
        nodes = self.env[self._name].search([('approval_flow_settings_id', '=', self.approval_flow_settings_id.id)])
        begin_node = None
        for node in nodes:
            if node.name == u'提交':
                begin_node = node
                break

        current_node = begin_node
        while current_node.parent_id != self:
            current_node = current_node.parent_id

        current_node.write({
            'parent_id': self.parent_id.id,
        })



    @api.multi
    def write(self, vals):
        res = super(Cowin_approval_flow_setting_node, self).write(vals)
        return res


    @api.multi
    def unlink(self):
        self._fix_dependency_at_unlink()
        return super(Cowin_approval_flow_setting_node, self).unlink()






