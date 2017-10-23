# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Cowin_settings_process(models.Model):
    _name = 'cowin_settings.process'

    name = fields.Char(string=u'流程名称')

    stage_ids = fields.One2many('cowin_settings.process_stage', 'process_id', string='Stage ids')

    module = fields.Char(string=u'模块')

    description = fields.Char(string=u'说明')



    # rpc调用方法,前端页面直接获取后端数据的所需要的方法,
    # 该方法对应的是当前model类中的一条实例对象
    def get_info(self):
        stages = []

        for stage in self.stage_ids:
            tmp_stage = {}
            tmp_stage['id'] = stage.id
            tmp_stage['name'] = stage.name
            tmp_stage['process_id'] = stage.process_id

            tmp_stage['tache_ids'] = []

            for tache in stage.tache_ids:
                tmp_tache = {}
                tmp_tache['id'] = tache.id
                tmp_tache['name'] = tache.name
                tmp_tache['unlock_condition'] = tache.unlock_condition
                tmp_tache['description'] = tache.description
                tmp_tache['state'] = tache.state
                tmp_tache['stage_id'] = tache.stage_id

                tmp_stage['tache_ids'].append(tmp_tache)

            stages.append(tmp_stage)

        result = {
            'id': self.id,
            'name': self.name,
            # 'module': self.module,
            # 'description': self.description,
            'stage_ids': stages
        }

        return result




    def get_infos(self):
        result = []
        objs = self.env['cowin_settings.process'].search([])
        for item in objs:
            tmp = {}
            tmp['name'] = item.name
            tmp['module'] = item.module
            tmp['description'] = item.description

            result.append(tmp)

        return result

