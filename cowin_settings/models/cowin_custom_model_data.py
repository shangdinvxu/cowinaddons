# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Cowin_custom_model_data(models.Model):
    _name = 'cowin_settings.custome_model_data'


    # name = fields.Char(string=u'ID')

    model_name = fields.Char(string=u'model ID')