# -*- coding: utf-8 -*-

from odoo import models, fields, api
class Cowin_project_subproject_conference_resolutions(models.Model):
    '''
        投资决策委员会会议表决票
    '''

    _name = 'cowin_project.sub_conference_resolutions'

    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    invest_manager_id = fields.Many2one('hr.employee', related='subproject_id.invest_manager_id', string=u'投资经理')



    voting_committee = fields.Date(string=u'投决会日期')

    members_of_voting_committee_ids = fields.Many2many('hr.employee', string=u'投决会委员')

    voting_opinion = fields.Text(string=u'表决意见')

    voter = fields.Char(string=u'表决人')

    @api.model
    def create(self, vals):
        tache = self._context['tache']

        sub_project_id = int(tache['sub_project_id'])

        # vals['meta_sub_project_id'] = meta_sub_project_id

        sub_tache_id = int(tache['sub_tache_id'])

        sub_tache = self.env['cowin_project.subproject_process_tache'].browse(sub_tache_id)

        vals['subproject_id'] = sub_project_id
        res = super(Cowin_project_subproject_conference_resolutions, self).create(vals)
        sub_tache.write({
            'res_id': res.id,
            'is_unlocked': True,
            'view_or_launch': True,
        })

        return res