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
    process_id=fields.Many2one('cowin_settings.process', related='stage_id.process_id')

    once_or_more = fields.Boolean(string=u'发起次数', default=True)

    model_name = fields.Char(string=u'自定义model的名字')




    def _check_parent_id(self, ids=[]):

        # 如果parent_id为空的情况下,到达了顶层
        if not self.parent_id.id:
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



    # 检查依赖的记录之间时候会有环的形成!!1
    def on_set_parent_id(self):
        ids = []
        print u'kkkk'
        return self._check_parent_id(ids)
