# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Cowin_project_subproject_opinion_book(models.Model):

    '''
        立项意见书
    '''
    _name = 'cowin_project.sub_opinion_book'


    subproject_id = fields.Many2one('cowin_project.cowin_subproject')


    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    invest_manager_id = fields.Many2one('hr.employee', related='subproject_id.invest_manager_id', string=u'投资经理')


    date_of_project = fields.Date(string=u'立项日期')

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

    project_mumbers = fields.Many2many('hr.employee', string=u'项目小组成员')

    # examine_and_verify = fields.Char(string=u'审核校验', default=u'未开始审核')

    partner_opinion = fields.Text(string=u'项目合伙人表决意见')
    business_director_option = fields.Text(string=u'业务总监表决意见')
    policy_making_committee = fields.Text(string=u'投资决策委员会意见')


    @api.model
    def create(self, vals):
        tache = self._context['tache']

        sub_project_id = int(tache['sub_project_id'])

        # vals['meta_sub_project_id'] = meta_sub_project_id

        sub_tache_id = int(tache['sub_tache_id'])

        sub_tache = self.env['cowin_project.subproject_process_tache'].browse(sub_tache_id)




        vals['subproject_id'] = sub_project_id
        res = super(Cowin_project_subproject_opinion_book, self).create(vals)
        sub_tache.write({
            'res_id': res.id,
            'is_unlocked': True,
            'view_or_launch': True,
        })


        return res







