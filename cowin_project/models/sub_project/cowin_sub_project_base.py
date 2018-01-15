# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Cowin_sub_project_base_status(models.Model):
    _name = 'cowin_project.base_status'




    inner_or_outer_status = fields.Selection([(1, u'内部调用'), (2, u'外部调用')], string=u'子工程中,实体的状态', default=1)




