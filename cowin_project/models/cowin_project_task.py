from odoo import models, fields, api


class cowin_project_task(models.Model):
    _name = 'cowin_project.cowin_project_task'

    name = fields.Char()

    project_id = fields.Many2one('cowin_project.cowin_project')
