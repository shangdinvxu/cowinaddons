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

    #
    meta_process_id = fields.Many2one('cowin_settings.process', string=u'元数据配置信息')

    stage_ids = fields.One2many('cowin_project.process_stage', 'process_id', string='Stage ids')

    module = fields.Char(string=u'模块')

    description = fields.Char(string=u'说明')

    category = fields.Char(string=u'流程配置分类')

    project_ids = fields.One2many('cowin_project.cowin_project', 'process_id', string=u'主工程信息')



    # 该实例方法用于获取一条数据信息
    def get_info(self, prev_or_post_investment=True):
        stages = []

        # 需要新的排序
        # asc_by_show_orders = sorted(self.stage_ids, key=lambda stage: stage.show_order)
        # asc_by_show_orders = self.env['cowin_project.process_stage'].search([('process_id', '=', self.id),
        #               ('prev_or_post_investment', '=', prev_or_post_investment)], order='show_order')

        # asc_by_show_orders = self.stage_ids.filtered(lambda s: s.prev_or_post_investment == prev_or_post_investment).sorted('show_order')
        asc_by_show_orders = self.stage_ids.filtered(lambda s: s.prev_or_post_investment == prev_or_post_investment)
        for stage in asc_by_show_orders:
            tmp_stage = {}
            tmp_stage['id'] = stage.id
            tmp_stage['name'] = stage.name
            tmp_stage['prev_or_post_investment'] = stage.prev_or_post_investment
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


    def create_process_info(self, meta_process_info, project_name):

        '''
            以及创建配置节点, 阶段节点, 环节节点, 审批流
        :param meta_process_info:
        :return:
        '''

        # 元配置信息setings中的环节
        meta_taches = [tache
                       for stage in meta_process_info['stage_ids']
                       for tache in stage['tache_ids']]

        # name = meta_process_info['name']
        name = u'%s %s' % (u'流程配置', project_name)
        module = meta_process_info['module']
        description = meta_process_info['description']
        category = meta_process_info['category']

        # 复制一份元数据信息
        process = self.create({
            'name': name,
            'module': module,
            'description': description,
            # 'category': category,
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

                    order_parent_name = tache_in_meta['order_parent_id']

                    for target in taches_res:
                        if target.name == order_parent_name:
                            tache_in_pro.write({
                                'order_parent_id': target.id,
                            })



        # 对依环节进行排序操作!!!
        taches_res[0].set_depency_order_by_sub_tache()

        return process





    def approval_launch_roles_flow_roles(self):

        # 投前 发起角色,审批角色
        prev_approval_flow_launch_roles_entities = set()
        prev_approval_flow_roles_entities = set()

        # 投后 发起角色,审批角色
        post_approval_flow_launch_roles_entities = set()
        post_approval_flow_roles_entities = set()

        for stage_entity in self.stage_ids:
            if stage_entity.prev_or_post_investment:
                for tache_entity in stage_entity.tache_ids:
                    for approval_flow_settings_entity in tache_entity.approval_flow_settings_ids:
                        prev_approval_flow_launch_roles_entities.add(approval_flow_settings_entity.approval_flow_setting_node_ids[0].operation_role_id)
                        prev_approval_flow_roles_entities |= set(e.operation_role_id for e in approval_flow_settings_entity.approval_flow_setting_node_ids[1:-1])
            else:
                for tache_entity in stage_entity.tache_ids:
                    for approval_flow_settings_entity in tache_entity.approval_flow_settings_ids:
                        post_approval_flow_launch_roles_entities.add(
                            approval_flow_settings_entity.approval_flow_setting_node_ids[0].operation_role_id)
                        post_approval_flow_roles_entities |= set(e.operation_role_id for e in  \
                            approval_flow_settings_entity.approval_flow_setting_node_ids[1:-1])


        return (prev_approval_flow_launch_roles_entities, prev_approval_flow_roles_entities,
                    post_approval_flow_launch_roles_entities, post_approval_flow_roles_entities)