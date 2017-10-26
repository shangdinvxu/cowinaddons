# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Cowin_Common(models.Model):
    _name = 'cowin_project.cowin_common'

    name = fields.Char(string=u'行业', required=True)

    _sql_constraints = [
        ('industry_key', 'UNIQUE (name)', u'行业名不能相同')
    ]





class Cowin_Attachment(models.Model):
    _inherit = 'ir.attachment'