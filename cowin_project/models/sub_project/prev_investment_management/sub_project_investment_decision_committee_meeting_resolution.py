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
    ownership_interest = fields.Integer(
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
        tache_info = self._context['tache']

        # sub_project_id = int(tache_info['sub_project_id'])

        sub_tache_id = int(tache_info['sub_tache_id'])
        meta_sub_project_id = int(tache_info['meta_sub_project_id'])
        meta_sub_project_entity = self.env['cowin_project.meat_sub_project'].browse(meta_sub_project_id)

        sub_project_id = meta_sub_project_entity.sub_project_ids.id

        target_sub_tache_entity = meta_sub_project_entity.sub_tache_ids.browse(sub_tache_id)

        vals['subproject_id'] = sub_project_id
        res = super(Cowin_project_subproject_investment_decision_committee_meeting_resolution, self).create(vals)
        target_sub_tache_entity.write({
            'res_id': res.id,
            # 'is_unlocked': True,
            'view_or_launch': True,
        })

        # 判断 发起过程 是否需要触发下一个子环节
        target_sub_tache_entity.check_or_not_next_sub_tache()

        # 触发下一个依赖子环节处于解锁状态
        # for current_sub_tache_entity in meta_sub_project_entity.sub_tache_ids:
        #     if current_sub_tache_entity.parent_id == target_sub_tache_entity:
        #         current_sub_tache_entity.write({
        #             'is_unlocked': True,
        #         })

        return res




    @api.multi
    def write(self, vals):

        # 获取之前得到的基金轮次
        prev = set(self.round_financing_and_Foundation_ids)

        result = super(Cowin_project_subproject_investment_decision_committee_meeting_resolution, self).write(vals)

        # 获取之后得到的基金轮次
        after = set(self.round_financing_and_Foundation_ids)


        diffs = after - prev


        # 接下来这条数据的作用在于对轮次基金实体中的meta_sub_project_id做关联对应
        for round_financing_and_Foundation in diffs:
            # 创建元子工程
            meta_sub_project = self.env['cowin_project.meat_sub_project'].create({
                'project_id': self.subproject_id.meta_sub_project_id.project_id.id,
            })


            round_financing_and_Foundation.write({
                'meta_sub_project_id': meta_sub_project.id,
            })



        # 处理暂缓的情况!!!
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

        return result



