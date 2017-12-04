# -*- coding: utf-8 -*-
from odoo import models, fields, api







class Cowin_sub_project_approval_flow_settings_records(models.Model):
    _name = 'cowin_project.sub_approval_flow_settings_record'

    '''
        审批记录!!!
    '''

    sub_approval_settings_id = fields.Many2one('cowin_project.sub_approval_flow_settings', string=u'子审批实体',
                                               ondelete="cascade")
    approval_person_id = fields.Many2one('hr.employee', string=u'审批人')
    approval_role_id = fields.Many2one('cowin_common.approval_role', string=u'审批角色')

    approval_result = fields.Char(string=u'审批结果')
    approval_opinion = fields.Text(string=u'审批意见')




    # 保存审批历史记录
    def get_info(self):

        res = {}
        res['sub_approval_settings_id'] = self.sub_approval_settings_id.id
        res['approval_person_id'] = self.approval_person_id.id
        res['approval_person'] = self.approval_person_id.name
        res['approval_role_id'] = self.approval_role_id.id
        res['approval_role_name'] = self.approval_role_id.name
        res['approval_result'] = self.approval_result
        res['approval_opinion'] = self.approval_opinion
        res['create_date'] = self.create_date

        return res





