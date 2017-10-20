# -*- coding: utf-8 -*-

from odoo import models, fields, api


class cowin_settings_process(models.Model):
    _name = 'cowin_settings_process'

    name = fields.Char()

    stage_ids = fields.One2many('cowin_settings_process_stage', 'process_id', string='Stage id')