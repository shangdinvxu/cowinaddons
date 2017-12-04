# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class Cowin_project_process(models.Model):
    u'''
        每个项目都有自己唯一的一个元配置信息实体的一份实例,
        注意: 元数据信息
    '''
    _name = 'cowin_project.process'

    name = fields.Char(string=u'流程名称')

    meta_process_id = fields.Many2one('cowin_settings.process', string=u'元数据配置信息')

    stage_ids = fields.One2many('cowin_project.process_stage', 'process_id', string='Stage ids')

    module = fields.Char(string=u'模块')

    description = fields.Char(string=u'说明')

    category = fields.Char(string=u'流程配置分类')



    # 该实例方法用于获取一条数据信息
    def get_info(self):
        stages = []

        # 需要新的排序
        # asc_by_show_orders = sorted(self.stage_ids, key=lambda stage: stage.show_order)
        asc_by_show_orders = self.env['cowin_project.process_stage'].search([('process_id', '=', self.id)],
                                                                             order='show_order asc')

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
                # parent_id 就是解锁条件
                tmp_tache['is_unlocked'] = tache.is_unlocked
                # 需要考虑到环节的父节点可能没有
                # tmp_tache['is_unlocked'] = True if not tache.parent_id else tache.parent_id.is_unlocked
                tmp_tache['is_unlocked'] = tache.is_unlocked
                tmp_tache['description'] = tache.description
                tmp_tache['state'] = tache.state
                tmp_tache['once_or_more'] = tache.once_or_more
                tmp_tache['view_or_launch'] = tache.view_or_launch
                tmp_tache['res_id'] = tache.res_id

                # tmp_tache['res_id'] = tache.res_id
                tmp_tache['model_name'] = tache.model_id.model_name
                tmp_tache['stage_id'] = tache.stage_id.id
                # tmp_tache['approval_flow_settings_info'] = []
                # for approval_flow_settings_entity in tache.approval_flow_settings_ids:
                #     tmp = {}
                #     tmp['approval_flow_settings_id'] = approval_flow_settings_entity.id
                #     tmp['name'] = approval_flow_settings_entity.name
                #     tmp['tache_id'] = approval_flow_settings_entity.tache_id.id
                #     tmp['approval_flow_nodes_info'] = []
                #     for approval_flow_node_entity in approval_flow_settings_entity.approval_flow_setting_node_ids:
                #         t = {}
                #         t['approval_flow_settings_node_id'] = approval_flow_node_entity.id
                #         t['approval_flow_settings_id'] = approval_flow_node_entity.approval_flow_settings_id.id
                #         t['parent_id'] = approval_flow_node_entity.parent_id.id
                #         t['operation_role_id'] = approval_flow_node_entity.operation_role_id.id
                #         t['order'] = approval_flow_node_entity.order
                #         t['accept'] = approval_flow_node_entity.accept
                #         t['reject'] = approval_flow_node_entity.reject
                #         t['put_off'] = approval_flow_node_entity.put_off
                #         t['name'] = approval_flow_node_entity.name
                #
                #         tmp['approval_flow_nodes_info'].append(t)
                #
                #     tmp_tache['approval_flow_settings_info'].append(tmp)

                tmp_stage['tache_ids'].append(tmp_tache)

            stages.append(tmp_stage)

        result = {
            'id': self.id,
            'name': self.name,
            'module': self.module,
            'description': self.description,
            'category': self.category,
            'stage_ids': stages
        }

        return result


    # 因为有依赖条件的限制,所以需要检验解锁条件对前端的显示的操作
    def _check_unlock_condition(self, info):

        for stage in info['stage_ids']:
            for tache in stage['tache_ids']:
                if not tache['is_unlocked']:
                    tache['once_or_more'] = False
                    tache['res_id'] = False




    # 该rpc方法用于获取所有的列表信息
    def get_infos(self):
        result = []
        objs = self.env['cowin_project.process'].search([])
        for item in objs:
            result.append({
                'name': item.name,
                'module': item.module,
                'description': item.description,
                "id": item.id
            })
        return result



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

    def get_tache_entity(self, tache_id):
        for tache in self.get_all_tache_entities():
            if tache.id == tache_id:
                return tache

    def get_approval_flow_settings(self):
        taches = self.get_all_taches()

    # 开始做审批流设置
    def rpc_approval_flow_setting(self, **kwargs):

        return self.get_info()

    def rpc_edit_approva_flow_settings(self, **kwargs):
        approval_flow_settings_id = int(kwargs.get('approval_flow_settings_id'))

        # 获得该审批流实体
        approval_flow_settings = self.env['cowin_project.approval_flow_settings'].browse(approval_flow_settings_id)

        res = approval_flow_settings.get_all_approval_flow_setting_nodes()

        return res


    def create_process_info(self, meta_process_info):

        '''
            以及创建配置节点, 阶段节点, 环节节点, 审批流
        :param meta_process_info:
        :return:
        '''

        # 元配置信息setings中的环节
        meta_taches = [tache
                       for stage in meta_process_info['stage_ids']
                       for tache in stage['tache_ids']]

        name = meta_process_info['name']
        module = meta_process_info['module']
        description = meta_process_info['description']
        category = meta_process_info['category']

        # 复制一份元数据信息
        process = self.create({
            'name': name,
            'module': module,
            'description': description,
            'category': category,
            'meta_process_id': meta_process_info['id'],
        })

        # 在该工程下的中的settings中的阶段
        # self.env['cowin_project.process_stage'].create_stage_info(meta_process_info, process.id)
        # 由于是创建的过程,所以这些stage_ids都会是为空的值,但是是一个空的record对象
        process.stage_ids.create_stage_info(meta_process_info, process.id)

        # 每个工程都有自己的配置的信息的环节实体
        taches_res = process.get_all_tache_entities()

        # 修复环节依赖的问题
        for tache_in_pro in taches_res:
            for tache_in_meta in meta_taches:
                if tache_in_pro.name == tache_in_meta['name']:
                    parent_name = tache_in_meta['parent_id']
                    for target in taches_res:
                        if target.name == parent_name:
                            tache_in_pro.write({
                                'parent_id': target.id
                            })




        return process





