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

    def _check_parent_id(self, parent_id, ids):
        parent = self.env['cowin_settings.process_tache'].browse(parent_id)
        if parent:
            if ids.contains(parent):
                return False
            if self.id != parent.id:
                if parent.parent_id:
                    ids.append(self.id)
                    ids.append(parent.id)
                    parent._check_parent_id(ids)
                else:
                    return True
            else:
                return False

    def on_set_parent_id(self, parent_id):
        ids = []
        if self._check_parent_id(self, parent_id, ids):
            self.parent_id = parent_id
