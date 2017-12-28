# -*- coding: utf-8 -*-
from odoo import models, fields, api


class sub_project_summary_of_the_three_meeting_of_the_item_company(models.Model):

    _name = 'cowin_project.sub_sum_of_the_three_meeting'

    '''
        项目公司三会纪要
    '''

    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')

    reporter = fields.Many2one('hr.employee', string=u'报告人')

    filing_date = fields.Datetime(string=u'提交日期')

    form_of_mettings = fields.Selection([(1, u'董事会'), (2, u'股东会'), (3, u'监事会')], string=u'会议形式')

    mettings_summary = fields.Text(string=u'会议纪要')

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



    @api.model
    def create(self, vals):
        tache_info = self._context['tache']

        sub_tache_id = int(tache_info['sub_tache_id'])
        meta_sub_project_id = int(tache_info['meta_sub_project_id'])
        meta_sub_project_entity = self.env['cowin_project.meat_sub_project'].browse(meta_sub_project_id)

        sub_project_id = meta_sub_project_entity.sub_project_ids.id

        target_sub_tache_entity = meta_sub_project_entity.sub_tache_ids.browse(sub_tache_id)

        vals['subproject_id'] = sub_project_id
        res = super(sub_project_summary_of_the_three_meeting_of_the_item_company, self).create(vals)
        target_sub_tache_entity.write({
            'res_id': res.id,
            # 'is_unlocked': True,
            'view_or_launch': True,
        })

        # 判断 发起过程 是否需要触发下一个子环节
        target_sub_tache_entity.check_or_not_next_sub_tache()

        return res

    @api.model
    def write(self, vals):
        res = super(sub_project_summary_of_the_three_meeting_of_the_item_company, self).write(vals)
        tache_info = self._context['tache']

        meta_sub_project_id = int(tache_info['meta_sub_project_id'])

        # 校验meta_sub_project所对应的子工程只能有一份实体
        meta_sub_project_entity = self.env['cowin_project.meat_sub_project'].browse(meta_sub_project_id)

        sub_tache_id = int(tache_info['sub_tache_id'])

        target_sub_tache_entity = meta_sub_project_entity.sub_tache_ids.browse(sub_tache_id)

        target_sub_tache_entity.write({
            'is_launch_again': False,
        })

        # 判断 发起过程 是否需要触发下一个子环节
        target_sub_tache_entity.check_or_not_next_sub_tache()

