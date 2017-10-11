# -*- coding: utf-8 -*-

from odoo import models, fields, api


class cowin_project(models.Model):
    _name = 'cowin_project.cowin_project'

    name = fields.Char()
