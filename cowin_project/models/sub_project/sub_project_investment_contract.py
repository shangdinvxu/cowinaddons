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