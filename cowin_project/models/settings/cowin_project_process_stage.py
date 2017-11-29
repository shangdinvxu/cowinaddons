# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError



class Cowin_settings_process_stage(models.Model):
    _name = 'cowin_project.process_stage'

    name = fields.Char(string=u'分组')
    show_order = fields.Integer(string=u'需要在前端界面显示的顺序',
                                default=lambda self: int(self.env['ir.sequence'].next_by_code('cowin_project_settings.order')))


    process_id = fields.Many2one('cowin_project.process', ondelete="cascade")

    tache_ids = fields.One2many('cowin_project.process_tache', 'stage_id', string='Tache ids')




        # 前端指定的顺序来显示

    def substitution_stage_by_show_order(self, target_stage):
        if self.show_order == target_stage.show_order:
            return

        self.show_order, target_stage.show_order = target_stage.show_order, self.show_order


    def create_stage_info(self, meta_stage_info, process_id):
        stages = meta_stage_info['stage_ids']

        for stage in stages:
            new_stage = self.create({
                'name': stage['name'],
                'show_order': int(stage['show_order']),
                'process_id': process_id,
            })

            for tache in stage['tache_ids']:
                # taches_res.append(self.env['cowin_project.process_tache'].create_tache_info(tache, new_stage.id))
                # self.env['cowin_project.process_tache'].create_tache_info(tache, new_stage.id)

                # 默认情况下,tache_ids也是只有一份数据
                new_stage.tache_ids.create_tache_info(tache, new_stage.id)

