# -*- coding: utf-8 -*-
from odoo import models, fields, api







class Cowin_sub_project_approval_flow_settings_records(models.Model):
    _name = 'cowin_project.approval_flow_settings_records'

    '''
        审批记录!!!
    '''

    sub_approval_flow_id = fields.Many2one('', string=u'子审批实体', ondelete="cascade")
    user_id = fields.Many2one('hr.employee', string=u'审批人')
    approval_role = fields.Many2one('cowin_common.approval_role', string=u'审批角色')

    approval_result = fields.Char(string=u'审批结果')
    approval_opinion = fields.Text(string=u'审批意见')