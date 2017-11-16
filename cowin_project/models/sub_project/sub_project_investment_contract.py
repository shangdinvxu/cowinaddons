# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Cowin_project_subproject_investment_contract(models.Model):
    '''
        投资合同
    '''

    _name = 'cowin_project.sub_invest_contract'

    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    contract_no = fields.Char(string=u'合同编号')
    title = fields.Char(string=u'标题')
    main_contents = fields.Text(string=u'主要内容')

    @api.model
    def create(self, vals):
        tache = self._context['tache']

        sub_project_id = int(tache['sub_project_id'])

        # vals['meta_sub_project_id'] = meta_sub_project_id

        sub_tache_id = int(tache['sub_tache_id'])

        sub_tache = self.env['cowin_project.subproject_process_tache'].browse(sub_tache_id)

        vals['subproject_id'] = sub_project_id
        res = super(Cowin_project_subproject_investment_contract, self).create(vals)
        sub_tache.write({
            'res_id': res.id,
            'is_unlocked': True,
            'view_or_launch': True,
        })

        return res