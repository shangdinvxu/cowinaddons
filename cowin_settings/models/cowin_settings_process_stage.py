# -*- coding: utf-8 -*-

from odoo import models, fields, api


class cowin_settings_process_stage(models.Model):
    _name = 'cowin_settings_process_stage'

    name = fields.Char()

    process_id = fields.Many2one('cowin_settings_process')
