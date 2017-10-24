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



    # rpc调用方法,前端页面直接获取后端数据的所需要的方法,
    # 该方法对应的是当前model类中的一条实例对象

    # 该实例方法用于获取一条数据信息
    def get_info(self):
        stages = []

        for stage in self.stage_ids:
            tmp_stage = {}
            tmp_stage['id'] = stage.id
            tmp_stage['name'] = stage.name
            tmp_stage['process_id'] = stage.process_id.id

            tmp_stage['tache_ids'] = []

            for tache in stage.tache_ids:
                tmp_tache = {}
                tmp_tache['id'] = tache.id
                tmp_tache['name'] = tache.name
                tmp_tache['parent_id'] = tache.parent_id.name
                tmp_tache['description'] = tache.description
                tmp_tache['state'] = tache.state
                tmp_tache['stage_id'] = tache.stage_id.id

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
                'name':item.name,
                'module':item.module,
                'description':item.description,
                "id": item.id
            })
        return result


    # 使用rpc方法来对该实例对象来建立新的分组数据
    def rpc_create_group(self, name):
        if not name:
            raise UserError('分组名不能为空!!!')

        stage = self.env['cowin_settings.process_stage'].create({'name':name,
                                                                 'process_id': self.id
                                                                 })
        return {'id': stage.id,
                'name': stage.name,
                'process_id': self.id
                }