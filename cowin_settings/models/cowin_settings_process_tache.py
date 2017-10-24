# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class Cowin_settings_process_tache(models.Model):
    _name = 'cowin_settings.process_tache'

    name = fields.Char(string=u'环节')

    parent_id = fields.Many2one('cowin_settings.process_tache', string=u'解锁条件')

    description = fields.Char(string=u'说明')

    state = fields.Boolean(string=u'启用状态', default=True)

    stage_id = fields.Many2one('cowin_settings.process_stage', ondelete="cascade")


    # 使用rpc来新建环节,但前提必须是stage对象需要存在
    def rpc_create_tache(self, stage_id, name):
        if not stage_id or not name:
            raise UserError('分组名或者环节名不能为空!!!')

        tache = self.env['cowin_settings.process_tache'].create({'name': name,
                                                        'stage_id': stage_id
                                                         })

        return {
            'id': tache.id,
            'name': tache.name,
            'stage_id': stage_id
        }