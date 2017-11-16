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
    invest_manager_id = fields.Many2one('hr.employee', related='subproject_id.invest_manager_id', string=u'投资经理')

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

    @api.model
    def create(self, vals):
        tache = self._context['tache']

        sub_project_id = int(tache['sub_project_id'])

        # vals['meta_sub_project_id'] = meta_sub_project_id

        sub_tache_id = int(tache['sub_tache_id'])

        sub_tache = self.env['cowin_project.subproject_process_tache'].browse(sub_tache_id)

        vals['subproject_id'] = sub_project_id
        res = super(Cowin_project_subproject_appointment_and_dismissal, self).create(vals)
        sub_tache.write({
            'res_id': res.id,
            'is_unlocked': True,
            'view_or_launch': True,
        })

        return res
