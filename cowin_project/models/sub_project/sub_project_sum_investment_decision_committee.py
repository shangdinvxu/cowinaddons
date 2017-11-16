# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Cowin_project_subproject_sum_investment_decision_committee(models.Model):
    '''
        投资决策委员会会议纪要
    '''

    _name = 'cowin_project.sub_sum_invest_decision_committee'

    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    invest_manager_id = fields.Many2one('hr.employee', related='subproject_id.invest_manager_id', string=u'投资经理')

    voting_committee_date = fields.Date(string=u'投决会日期')

    conference_recorder = fields.Many2one('hr.employee', string=u'会议记录人')
    checker = fields.Many2one('hr.employee', string=u'复核人')
    investment_decision_committee = fields.Many2many('hr.employee', string=u'投资决策委员')

    conference_highlights = fields.Text(string=u'会议要点')



    @api.model
    def create(self, vals):
        tache = self._context['tache']

        sub_project_id = int(tache['sub_project_id'])

        # vals['meta_sub_project_id'] = meta_sub_project_id

        sub_tache_id = int(tache['sub_tache_id'])

        sub_tache = self.env['cowin_project.subproject_process_tache'].browse(sub_tache_id)




        vals['subproject_id'] = sub_project_id
        res = super(Cowin_project_subproject_sum_investment_decision_committee, self).create(vals)
        sub_tache.write({
            'res_id': res.id,
            'is_unlocked': True,
            'view_or_launch': True,
        })


        return res
