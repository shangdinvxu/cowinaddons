# -*- coding: utf-8 -*-

from odoo import models, fields, api


class cowin_settings_process_tache(models.Model):
    _name = 'cowin_settings_process_tache'

    name = fields.Char()

    stage_id = fields.Many2one('cowin_settings_process_stage')
