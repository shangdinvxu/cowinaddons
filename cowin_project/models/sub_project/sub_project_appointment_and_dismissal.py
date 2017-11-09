# -*- coding: utf-8 -*-
from odoo import models, fields, api
class Cowin_project_subproject_appointment_and_dismissal(models.Model):

    '''

        董事／监事任免书
    '''

    _name = 'cowin_project.sub_appointment_and_dismissal'

    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    invest_manager = fields.Many2one(related='subproject_id.invest_manager', string=u'投资经理')

    #----- 任免对象
    trustee = fields.Many2one('hr.employee', string=u'董事')
    appointment_time_begin_trustee = fields.Date()
    appointment_time_end_trustee = fields.Date()

    Tenure_trustee = fields.Float(string=u'任职年限')

    supervisor = fields.Many2one('hr.employee', string=u'监事')
    appointment_time_begin_supervisor = fields.Date()
    appointment_time_endr_supervisor = fields.Date()

    Tenure_supervisor = fields.Float(string=u'任职年限')




    #------

    managing_partner = fields.Many2one('hr.employee', string=u'管理合伙人')
