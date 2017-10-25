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

    once_or_more = fields.Boolean(string=u'发起次数', default=True)


    def _check_parent_id(self, ids=[]):

        # 如果parent_id为空的情况下,到达了顶层
        if not self.parent_id.id or not ids:
            return True

        # 如果parent_id不为空的, 相互引用的话,直接返回为False
        # 不过,这里情况可以包含在抽象递归调用之中
        # if self.id == self.parent_id.id:
        #     return False

        # 如果便利的节点的列表为空的情况下,直接返回True
        # if not ids:
        #     return True

        if self.id in ids:
            return False

        ids.append(self.id)

        return self.parent_id._check_parent_id(ids)




        # if parent:
        #     # if ids.contains(parent.id):
        #     if parent.id in ids:
        #         return False
        #     if self.id != parent.id:
        #         if parent.parent_id:
        #             ids.append(self.id)
        #             # ids.append(parent.id)
        #             return parent._check_parent_id(parent.id, ids)
        #         else:
        #
        #             return True
        #     else:
        #         return False
        # return False

    def on_set_parent_id(self):
        ids = []
        return self._check_parent_id()