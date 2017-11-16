# -*- coding: utf-8 -*-
from odoo import models, fields, api
class Cowin_project_subproject_project_entrusted_loan_application_form(models.Model):
    '''
        项目委托贷款申请表
    '''

    _name = 'cowin_project.sub_entrusted_loan_app_form'

    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    invest_manager_id = fields.Many2one('hr.employee', related='subproject_id.invest_manager_id', string=u'投资经理')

    date_of_application = fields.Date(string=u'申请日期')

    # ----------  投资基金
    round_financing_id = fields.Many2one('cowin_common.round_financing',
                                         related='subproject_id.round_financing_id', string=u'轮次')

    foundation_id = fields.Many2one('cowin_foundation.cowin_foudation',
                                    related='subproject_id.foundation_id', string=u'基金')

    the_amount_of_financing = fields.Float(
        related='subproject_id.the_amount_of_financing', string=u'本次融资额')

    the_amount_of_investment = fields.Float(
        related='subproject_id.the_amount_of_investment', string=u'本次投资金额')
    ownership_interest = fields.Float(
        related='subproject_id.ownership_interest', string=u'股份比例')
    # ---------------

    list_of_examination_and_approval_documents = fields.Many2many('ir.attachment', string=u'审批文件清单')

    time_of_application_for_entrusted_loan = fields.Date(string=u'委托贷款申请时间')
    amount_of_application_for_entrusted_loan = fields.Float(string=u'委托贷款申请金额')
    reasons_for_application = fields.Text(string=u'申请原因')
    entrusted_loan_bank = fields.Char(string=u'委托贷款银行')
    lending_rate = fields.Float(string=u'借款利率')
    life_of_loan = fields.Float(string=u'借款期限')
    transfer_charge = fields.Float(string=u'手续费')

    @api.model
    def create(self, vals):
        tache = self._context['tache']

        sub_project_id = int(tache['sub_project_id'])

        # vals['meta_sub_project_id'] = meta_sub_project_id

        sub_tache_id = int(tache['sub_tache_id'])

        sub_tache = self.env['cowin_project.subproject_process_tache'].browse(sub_tache_id)

        vals['subproject_id'] = sub_project_id
        res = super(Cowin_project_subproject_project_entrusted_loan_application_form, self).create(vals)
        sub_tache.write({
            'res_id': res.id,
            'is_unlocked': True,
            'view_or_launch': True,
        })

        return res




