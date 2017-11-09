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