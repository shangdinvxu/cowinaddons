# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json
from odoo.exceptions import UserError


class Cowin_settings_process(models.Model):
    _name = 'cowin_settings.process'

    name = fields.Char(string=u'流程名称')

    stage_ids = fields.One2many('cowin_settings.process_stage', 'process_id', string='Stage ids')

    module = fields.Char(string=u'模块')

    description = fields.Char(string=u'说明')

    category = fields.Char(string=u'流程配置分类')


    # 该实例方法用于获取一条数据信息
    def get_info(self):
        stages = []

        # 需要新的排序
        # asc_by_show_orders = sorted(self.stage_ids, key=lambda stage: stage.show_order)
        asc_by_show_orders = self.env['cowin_settings.process_stage'].search([('process_id', '=', self.id)],
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
                tmp_tache['description'] = tache.description
                tmp_tache['state'] = tache.state
                tmp_tache['once_or_more'] = tache.once_or_more
                tmp_tache['model_name'] = tache.model_name.model_name
                tmp_tache['stage_id'] = tache.stage_id.id
                tmp_tache['approval_flow_settings_id'] = tache.approval_flow_settings.id

                tmp_stage['tache_ids'].append(tmp_tache)

            stages.append(tmp_stage)

        result = {
            'id': self.id,
            'name': self.name,
            'stage_ids': stages
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

        tache_id = kwargs.get('tache_id')
        name = kwargs.get('tache_name')
        tache_parent_id = int(kwargs.get('tache_parent_id')) if kwargs.get('tache_parent_id') else None

        description = kwargs.get('description')

        tache = self.env['cowin_settings.process_tache'].browse(int(tache_id))
        tache.write({'name': name,
                     'parent_id': tache_parent_id,
                     'description': description
                     })

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


    def get_approval_flow_settings(self):
        taches = self.get_all_taches()




    # 开始做审批流设置
    def rpc_approval_flow_setting(self, **kwargs):



        return self.get_info()



    def rpc_edit_approva_flow_settings(self, **kwargs):
        approval_flow_settings_id = int(kwargs.get('approval_flow_settings_id'))

        # 获得该审批流实体
        approval_flow_settings = self.env['cowin_settings.approval_flow_settings'].browse(approval_flow_settings_id)

        res = approval_flow_settings.get_all_approval_flow_setting_nodes()

        return res