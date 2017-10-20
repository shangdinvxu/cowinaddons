# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Cowin_settings_process_stage(models.Model):
    _name = 'cowin_settings.process_stage'

    name = fields.Char(string=u'分组')

    process_id = fields.Many2one('cowin_settings.process', ondelete="cascade")

    tache_ids = fields.One2many('cowin_settings.process_tache', 'stage_id', string='Tache ids')
