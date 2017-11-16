# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Cowin_project_subproject_investment_decision_committee_meeting_resolution(models.Model):

    '''
        投资决策委员会会议决议
    '''
    _name = 'cowin_project.sub_invest_decision_committee_res'

    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    invest_manager_id = fields.Many2one('hr.employee', related='subproject_id.invest_manager_id', string=u'投资经理')

    voting_committee = fields.Date(string=u'投决会日期')
    outcome_of_the_voting_committee = fields.Char(string=u'投决会结果')

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



    round_financing_and_Foundation_ids = fields.One2many('cowin_project.round_financing_and_foundation',
                                                         'sub_invest_decision_committee_res_id',
                                                         string=u'添加基金')


    trustee = fields.Many2one('hr.employee', string=u'董事')
    supervisor = fields.Many2one('hr.employee', string=u'监事')
    amount_of_entrusted_loan = fields.Float(string=u'委托贷款金额')
    chairman_of_investment_decision_committee = fields.Many2one('hr.employee', string=u'投资决策委员会主席')



    @api.model
    def create(self, vals):
        tache = self._context['tache']

        sub_project_id = int(tache['sub_project_id'])

        # vals['meta_sub_project_id'] = meta_sub_project_id

        sub_tache_id = int(tache['sub_tache_id'])

        sub_tache = self.env['cowin_project.subproject_process_tache'].browse(sub_tache_id)

        vals['subproject_id'] = sub_project_id
        res = super(Cowin_project_subproject_investment_decision_committee_meeting_resolution, self).create(vals)

        sub_tache.write({
            'res_id': res.id,
            'is_unlocked': True,
            'view_or_launch': True,
        })



        # 接下来这条数据的作用在于对轮次基金实体中的meta_sub_project_id做关联对应
        for round_financing_and_Foundation in res.round_financing_and_Foundation_ids:
            # 创建元子工程
            meta_sub_project = self.env['cowin_project.meat_sub_project'].create({
                'project_id': res.subproject_id.meta_sub_project_id.project_id.id,
            })


            round_financing_and_Foundation.write({
                'meta_sub_project_id': meta_sub_project.id,
            })


        return res





