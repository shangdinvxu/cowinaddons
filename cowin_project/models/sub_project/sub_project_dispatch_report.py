# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Cowin_project_subproject_dispatch_report(models.Model):

    '''
        尽调报告
    '''

    _name = 'cowin_project.subt_dispatch_report'

    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    dispatch_report = fields.Many2many('ir.attachment', string=u'尽调报告')

    attachment_note = fields.Char(string=u'附件说明')

    @api.model
    def create(self, vals):
        tache = self._context['tache']

        sub_project_id = int(tache['sub_project_id'])

        # vals['meta_sub_project_id'] = meta_sub_project_id

        sub_tache_id = int(tache['sub_tache_id'])

        sub_tache = self.env['cowin_project.subproject_process_tache'].browse(sub_tache_id)

        vals['subproject_id'] = sub_project_id
        res = super(Cowin_project_subproject_dispatch_report, self).create(vals)
        sub_tache.write({
            'res_id': res.id,
            'is_unlocked': True,
            'view_or_launch': True,
        })

        return res