# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json
from odoo.exceptions import UserError
import uuid


class Cowin_settings_process(models.Model):
    _name = 'cowin_settings.process'

    name = fields.Char(string=u'流程名称')

    stage_ids = fields.One2many('cowin_settings.process_stage', 'process_id', string='Stage ids')

    module = fields.Char(string=u'模块')

    description = fields.Char(string=u'说明')

    category = fields.Char(string=u'流程配置分类')

    _sql_constraints = [
        ('name_key', 'UNIQUE (name)', u'流程配置名不能相同!!!')
    ]

    # 对当前的节点以及子孙节点进行拷贝,手动获取数据信息
    # 慎重考虑,考虑到以后的简便性,不适用字典的方式
    def copy_custom(self):
        return self.get_info()


    # 该实例方法用于获取一条数据信息
    def get_info(self):
        stages = []

        # 需要新的排序
        # asc_by_show_orders = sorted(self.stage_ids, key=lambda stage: stage.show_order)
        # asc_by_show_orders = self.env['cowin_settings.process_stage'].search([('process_id', '=', self.id)],
        #                                                                      order='show_order asc')

        asc_by_show_orders = self.stage_ids.sorted('show_order')



        for stage in asc_by_show_orders:
            tmp_stage = {}
            tmp_stage['id'] = stage.id
            tmp_stage['name'] = stage.name
            tmp_stage['show_order'] = stage.show_order
            tmp_stage['process_id'] = stage.process_id.id

            tmp_stage['tache_ids'] = []

            for tache in stage.tache_ids:
                tmp_tache = {}
                tmp_tache['id'] = tache.id
                tmp_tache['name'] = tache.name
                tmp_tache['parent_id'] = tache.parent_id.name
                tmp_tache['order_parent_id'] = tache.order_parent_id.name
                # parent_id 就是解锁条件
                # tmp_tache['is_unlocked'] = tache.parent_id.is_unlocked
                # 需要考虑到环节的父节点可能没有
                tmp_tache['is_unlocked'] = True if not tache.parent_id.id else tache.parent_id.is_unlocked
                tmp_tache['description'] = tache.description
                tmp_tache['state'] = tache.state
                tmp_tache['once_or_more'] = tache.once_or_more
                tmp_tache['model_name'] = tache.model_id.model_name
                tmp_tache['stage_id'] = tache.stage_id.id
                tmp_tache['approval_flow_settings_info'] = []
                for approval_flow_settings_entity in tache.approval_flow_settings_ids:
                    tmp = {}
                    tmp['approval_flow_settings_id'] = approval_flow_settings_entity.id
                    tmp['name'] = approval_flow_settings_entity.name
                    tmp['tache_id'] = approval_flow_settings_entity.tache_id.id
                    tmp['approval_flow_nodes_info'] = []
                    for approval_flow_node_entity in approval_flow_settings_entity.approval_flow_settings_node_ids:
                        t = {}
                        t['approval_flow_settings_node_id'] = approval_flow_node_entity.id
                        t['name'] = approval_flow_node_entity.name
                        t['approval_flow_settings_id'] = approval_flow_node_entity.approval_flow_settings_id.id
                        t['parent_id'] = approval_flow_node_entity.parent_id.id
                        t['operation_role_id'] = approval_flow_node_entity.operation_role_id.id
                        t['order'] = approval_flow_node_entity.order
                        t['accept'] = approval_flow_node_entity.accept
                        t['reject'] = approval_flow_node_entity.reject
                        t['put_off'] = approval_flow_node_entity.put_off

                        tmp['approval_flow_nodes_info'].append(t)

                    tmp_tache['approval_flow_settings_info'].append(tmp)

                tmp_stage['tache_ids'].append(tmp_tache)

            stages.append(tmp_stage)

        # tache_name_infos = [{'id': 0, 'name': u'无条件'}]
        tache_name_infos = []

        tmps = self.get_all_tache_entities_in_big().read(['name', 'parent_id'])

        tache_name_infos.extend({'id': k['id'] , 'name': k['name']} for k in tmps)
        tache_name_infos.extend({'id': k['parent_id'][0], 'name': k['parent_id'][1]} for k in tmps if k['parent_id'])

        # 去重操作

        union_tmps = []
        for i in tache_name_infos:
            if not i in union_tmps:
                union_tmps.append(i)



        result = {
            'id': self.id,
            'name': self.name,
            'module': self.module,
            'description': self.description,
            'category': self.category,
            'stage_ids': stages,
            'tache_name_infos': union_tmps,
        }

        return result

    # 该rpc方法用于获取所有的列表信息
    def get_infos(self):
        result = []
        objs = self.env['cowin_settings.process'].search([])
        for item in objs:
            result.append({
                'name': item.name,
                'module': item.module,
                'description': item.description,
                "id": item.id
            })
        return result



     # 使用rpc方法来对该实例对象来建立新的分组数据
    def rpc_create_group(self, **kwargs):
        '''
            kwargs参数中
                name 分组名
                show_order 前端显示顺序序号
        :param kwargs:
        :return:
        '''

        if not kwargs.get('name') or not kwargs.get('process_id'):
            raise UserError('分组名不能为空!!!')

        source = self.env['cowin_settings.process_stage'].create({'name': kwargs.get("name"),
                                                                 'process_id': kwargs.get("process_id")
                                                                       })
        return self.get_info()


    def rpc_edit_group(self, **kwargs):
        '''
        name 分组名
        stage_id: 分组id
        :param kwargs:
        :return:
        '''

        id = kwargs.get('stage_id')
        name = kwargs.get('name')
        if not name:
            raise UserError(u'分组名不能为空!!!')
        self.env['cowin_settings.process_stage'].search([('id', '=', id)]).write({'name': name})
        return self.get_info()


    # 使用rpc方法来对删除分组所对应的实例(记录)
    def rpc_delete_group(self, **kwargs):
        id = kwargs.get('stage_id')
        self.env['cowin_settings.process_stage'].search([('id', '=', id)]).unlink()

        return self.get_info()


    # 使用rpc来新建环节,但前提必须是stage对象需要存在
    def rpc_create_tache(self, **kwargs):
        if not kwargs.get('name') or not kwargs.get('stage_id'):
            raise UserError('环节名不能为空!!!')

        self.env['cowin_settings.process_tache'].create({'name': kwargs.get('name'),
                                                        'stage_id': kwargs.get('stage_id'),
                                                        'description': kwargs.get('description'),
                                                        'once_or_more': kwargs.get('once_or_more'),
                                                         })

        return self.get_info()



    # 使用rpc来删除环节记录(实体)
    def rpc_delete_tache(self, **kwargs):
        id = kwargs.get('tache_id')
        self.env['cowin_settings.process_tache'].search([('id', '=', id)]).unlink()

        return self.get_info()

    # 使用rpc来编辑环节名称
    def rpc_edit_tache(self, **kwargs):
        # 可能需要解锁依赖环的问题
        try:
            self.rpc_unlock_condition(**kwargs)
        except UserError, e:
            raise UserError(u'编辑过程中 解锁条件之间冲突行成环状')

        # 注意,环节中的所属分组不能是项目设立,因为有子环节的概念!!! (在工程处理讨论中)





        tache_id = kwargs.get('tache_id')
        once_or_more = kwargs.get('once_or_more')
        name = kwargs.get('tache_name')
        stage_id = kwargs.get('stage_id')
        tache_parent_id = int(kwargs.get('tache_parent_id')) if kwargs.get('tache_parent_id') else None





        # if tache_parent_id is None:
        #     # 考虑到需要过滤到主工程环节
        #
        #     tache_entity = [tache_entity for tache_entity in self.get_all_tache_entities()
        #                       if not tache_entity.model_id.model_name == 'cowin_project.sub_payment_app_form'][0]
        #     tache_parent_id = tache_entity.id


        description = kwargs.get('description')

        tache_entity = self.env['cowin_settings.process_tache'].browse(int(tache_id))
        tache_entity.write({'name': name,
                     'once_or_more': once_or_more,
                     'parent_id': tache_parent_id,
                     'description': description,
                     'stage_id': stage_id
                     })

        # if not tache_entity.parent_id:
        #     raise UserError(u'所属分组不能够位于最顶级分组中!!!')
        #
        # if tache_entity.model_id.model_name == "cowin_project.cowin_subproject":
        #     raise UserError(u'项目立项不能发起多次!!!')

        return self.get_info()






    def rpc_unlock_condition(self,  **kwargs):
        tache_id = kwargs.get('tache_id')
        tache_parent_id = kwargs.get('tache_parent_id')

        tache = self.env['cowin_settings.process_tache'].search([('id', '=', tache_id)])

        # 环节的前置条件可以设置为空
        if not tache_parent_id:
            tache.write({'parent_id': None})
            return self.get_info()
        else:
            tache_parent = self.env['cowin_settings.process_tache'].search([('id', '=', tache_parent_id)])

            # 先把之前的父类数据保存下来
            tmp = tache.parent_id
            tache.parent_id = tache_parent

            if tache.on_set_parent_id():
                tache.write({'parent_id': tache_parent_id})
                return self.get_info()
            else:
                tache.write({'parent_id': tmp.id})
                raise UserError(u'解锁条件之间冲突行成环状!!!')



    # # 前端指定的顺序来显示
    # def _substitution_stage(self, source_stage, target_stage):
    #     if source_stage.id == target_stage.id:
    #         return
    #
    #     source_stage.show_order, target_stage.show_order = source_stage.show_order, target_stage.show_order
    #

    def rpc_save_order_by_stage(self, **kwargs):
        '''
            show_status: 传递过来的大字典 {stage_id1: show_order1, stage_id2: show_order2 ...}
                字典中的内容:
                stage_id*:   阶段的id
                show_order*: 每个阶段显示的位置
        :param kwargs:
        :return:
        '''

        show_status = kwargs.get('show_status')
        for stage_id, show_order in show_status.items():
            stage = self.env['cowin_settings.process_stage'].browse(int(stage_id))
            stage.write({'show_order': int(show_order)})

        return self.get_info()


    def get_all_taches(self):
        result = self.get_info()

        taches = [tache for stage in result['stage_ids']
                  for tache in stage['tache_ids']]

        return taches


    def get_all_tache_entities(self):
        return [tache
                 for stage in self.stage_ids
                 for tache in stage.tache_ids
                 ]

    def get_all_tache_entities_in_big(self):
        return reduce(lambda x, y: x | y, self.get_all_tache_entities())


    # 数据的转发都是通过元配置的来触发!!!

    # 开始做审批流设置
    def rpc_get_approval_flow_setting_info(self, **kwargs):
        tache_id = int(kwargs.get('tache_id'))
        # return self._get_approval_flow_settings_info(tache_id)

        for tache in self.get_all_tache_entities():
            if tache.id == tache_id:
                return tache.get_approval_flow_settings_info()


    def rpc_save_approval_flow_setting_info(self, **kwargs):
        tache_id = int(kwargs.get('tache_id'))
        # 添加,删除,修改的节点
        approval_flow_setting_nodes_info = kwargs.get('approval_flow_setting_nodes')
        for tache in self.get_all_tache_entities():
            if tache.id == tache_id:
                tache.save_approval_flow_settings_info(approval_flow_setting_nodes_info)
                return {'result': 'success'}





    # def approval_launch_roles_flow_roles(self):
    #
    #     # 投前 发起角色,审批角色
    #     prev_approval_flow_launch_roles_entities = []
    #     prev_approval_flow_roles_entities = []
    #
    #     # 投后 发起角色,审批角色
    #     post_approval_flow_launch_roles_entities = []
    #     post_approval_flow_roles_entities = []
    #
    #     for stage_entity in self.stage_ids:
    #         if stage_entity.prev_or_post_investment:
    #             for tache_entity in stage_entity.tache_ids:
    #                 for approval_flow_settings_entity in tache_entity.approval_flow_settings_ids:
    #                     prev_approval_flow_launch_roles_entities.append(approval_flow_settings_entity.approval_flow_settings_node_ids[0])
    #                     prev_approval_flow_roles_entities.extend(approval_flow_settings_entity.approval_flow_settings_node_ids[1:-1])
    #         else:
    #             for tache_entity in stage_entity.tache_ids:
    #                 for approval_flow_settings_entity in tache_entity.approval_flow_settings_ids:
    #                     post_approval_flow_launch_roles_entities.append(
    #                         approval_flow_settings_entity.approval_flow_settings_node_ids[0])
    #                     post_approval_flow_roles_entities.extend(
    #                         approval_flow_settings_entity.approval_flow_settings_node_ids[1:-1])
    #
    #
    #     return (prev_approval_flow_launch_roles_entities, prev_approval_flow_roles_entities,
    #                 post_approval_flow_launch_roles_entities, post_approval_flow_roles_entities)