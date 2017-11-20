# -*- coding: utf-8 -*-


from odoo import models, fields, api

class Cowin_settings_approval_role(models.Model):

    _name = 'cowin_settings.approval_role'

    '''
        审批角色
    '''


    name = fields.Char(string=u'角色名')





    _sql_constraints = [
        ('name_key', 'UNIQUE (name)', u'审批角色名称不能相同!!!'),
    ]

