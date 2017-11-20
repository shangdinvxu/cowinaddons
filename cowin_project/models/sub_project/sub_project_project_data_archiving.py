# -*- coding: utf-8 -*-
from odoo import models, fields, api
class Cowin_project_subproject_project_data_archiving(models.Model):

    '''
        项目资料归档
    '''

    _name = 'cowin_project.sub_project_data_archiving'



    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    invest_manager_id = fields.Many2one('hr.employee', related='subproject_id.invest_manager_id', string=u'投资经理')

    engagement_partner_id = fields.Many2one('hr.employee', string=u'项目合伙人')

    # ----------  投资基金
    round_financing_id = fields.Many2one('cowin_common.round_financing',
                                         related='subproject_id.round_financing_id', string=u'轮次')

    foundation_id = fields.Many2one('cowin_foundation.cowin_foudation',
                                    related='subproject_id.foundation_id', string=u'基金')

    the_amount_of_financing = fields.Float(
        related='subproject_id.the_amount_of_financing', string=u'本次融资额')

    the_amount_of_investment = fields.Float(
        related='subproject_id.the_amount_of_investment', string=u'本次投资金额')
    ownership_interest = fields.Integer(
        related='subproject_id.ownership_interest', string=u'股份比例')
    # ---------------



    investment_decision_process_information = fields.Many2many('ir.attachment', string=u'投资决策流程资料')
    relevant_legal_documents_and_materials = fields.Many2many('ir.attachment', string=u'相关法律文件资料')
    government_approval_materials = fields.Many2many('ir.attachment', string=u'政府审批资料')
    payment_process_information = fields.Many2many('ir.attachment', string=u'付款流程资料')
    business_change_data = fields.Many2many('ir.attachment', string=u'工商变更资料')

    @api.model
    def create(self, vals):
        tache = self._context['tache']

        sub_project_id = int(tache['sub_project_id'])

        # vals['meta_sub_project_id'] = meta_sub_project_id

        sub_tache_id = int(tache['sub_tache_id'])

        sub_tache = self.env['cowin_project.subproject_process_tache'].browse(sub_tache_id)

        vals['subproject_id'] = sub_project_id
        res = super(Cowin_project_subproject_project_data_archiving, self).create(vals)
        sub_tache.write({
            'res_id': res.id,
            'is_unlocked': True,
            'view_or_launch': True,
        })

        return res

