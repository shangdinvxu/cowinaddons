# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError



class Cowin_settings_process_stage(models.Model):
    _name = 'cowin_settings.process_stage'

    name = fields.Char(string=u'分组')
    show_order = fields.Integer(string=u'需要在前端界面显示的顺序',
                                default=lambda self: int(self.env['ir.sequence'].next_by_code('cowin_settings.order')))


    process_id = fields.Many2one('cowin_settings.process', ondelete="cascade")

    tache_ids = fields.One2many('cowin_settings.process_tache', 'stage_id', string='Tache ids')

    _sql_constraints = [
        ('login_key', 'UNIQUE (name)', u'阶段配置名不能相同!!!')
    ]


    # 前端指定的顺序来显示
    def substitution_stage_by_show_order(self, target_stage):
        if self.show_order == target_stage.show_order:
            return

        self.show_order, target_stage.show_order = target_stage.show_order, self.show_order
