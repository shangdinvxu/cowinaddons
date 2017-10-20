# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Cowin_settings_process(models.Model):
    _name = 'cowin_settings.process'

    name = fields.Char(string=u'项目设立进度')

    stage_ids = fields.One2many('cowin_settings.process_stage', 'process_id', string='Stage ids')