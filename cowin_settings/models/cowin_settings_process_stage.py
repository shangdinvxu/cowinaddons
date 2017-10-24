# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class Cowin_settings_process_stage(models.Model):
    _name = 'cowin_settings.process_stage'

    name = fields.Char(string=u'分组')

    process_id = fields.Many2one('cowin_settings.process', ondelete="cascade")

    tache_ids = fields.One2many('cowin_settings.process_tache', 'stage_id', string='Tache ids')


    # 使用rpc方法来对该实例对象来建立新的分组数据
    def rpc_create_group(self, **kwargs):
        stage = self.env['cowin_settings.process_stage'].create({'name': kwargs.get("name"),
                                                                 'process_id': kwargs.get("process_id")
                                                                 })

        return {
                'id': stage.id,
                'name': stage.name,
                'process_id': self.id or ''
            }
