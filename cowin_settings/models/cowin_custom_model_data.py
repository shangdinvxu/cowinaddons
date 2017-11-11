# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Cowin_custom_model_data(models.Model):
    _name = 'cowin_settings.custome_model_data'


    # name = fields.Char(string=u'ID')

    model_name = fields.Char(string=u'model ID')

    _sql_constraints = [
        ('model_name_key', 'UNIQUE (model_name)', u'model_name标识名不能相同!!!')
    ]