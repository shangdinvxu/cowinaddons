# -*- coding: utf-8 -*-
from odoo import models, fields, api







class Cowin_sub_project_approval_flow_settings_records(models.Model):
    _name = 'cowin_project.approval_flow_settings_records'

    '''
        审批流操作记录!!!
    '''


    user_id = fields.Many2one('res.users', string=u'审批人')
    name = fields.Many2one('cowin_common.approval_role', related='approval_flow_user_id', string=u'审批角色')