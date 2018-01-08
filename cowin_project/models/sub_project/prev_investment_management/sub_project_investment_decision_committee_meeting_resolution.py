# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Cowin_project_subproject_investment_decision_committee_meeting_resolution(models.Model):

    '''
        投资决策委员会会议决议
    '''
    _name = 'cowin_project.sub_invest_decision_committee_res'

    subproject_id = fields.Many2one('cowin_project.cowin_subproject', ondelete="cascade")

    # name = fields.Char(related='subproject_id.name', string=u"项目名称")
    # project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    # invest_manager_id = fields.Many2one('hr.employee', related='subproject_id.invest_manager_id', string=u'投资经理')

    name = fields.Char(string=u"项目名称")
    project_number = fields.Char(string=u'项目编号')
    invest_manager_id = fields.Many2one('hr.employee', string=u'投资经理')

    voting_committee = fields.Date(string=u'投决会日期')
    outcome_of_the_voting_committee = fields.Char(string=u'投决会结果')

    # ----------  投资基金

    # round_financing_and_foundation_id = fields.Many2one('cowin_project.round_financing_and_foundation',
    #                                                     related='subproject_id.round_financing_and_foundation_id',
    #                                                     string=u'基金轮次实体')
    round_financing_id = fields.Many2one('cowin_common.round_financing', string=u'融资轮次')
    foundation_id = fields.Many2one('cowin_foundation.cowin_foudation', string=u'基金名称')
    the_amount_of_financing = fields.Float(string=u'本次融资金额')
    the_amount_of_investment = fields.Float(string=u'本次投资金额')
    ownership_interest = fields.Integer(string=u'股份比例')

    compute_round_financing_and_foundation_id = fields.Char(compute=u'_compute_value')

    @api.depends('round_financing_id', 'foundation_id', 'the_amount_of_financing', 'the_amount_of_investment',
                 'ownership_interest', 'trustee_id', 'supervisor_id', 'amount_of_entrusted_loan')
    def _compute_value(self):
        for rec in self:
            rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].round_financing_id = rec.round_financing_id
            rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].foundation_id = rec.foundation_id
            rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].the_amount_of_financing = rec.the_amount_of_financing
            rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].the_amount_of_investment = rec.the_amount_of_investment
            rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].ownership_interest = rec.ownership_interest

            rec.subproject_id.trustee_id = rec.trustee_id
            rec.subproject_id.supervisor_id = rec.supervisor_id
            rec.subproject_id.amount_of_entrusted_loan = rec.amount_of_entrusted_loan

    # round_financing_id = fields.Many2one('cowin_common.round_financing',
    #                                      related='subproject_id.round_financing_id', string=u'轮次')
    #
    # foundation_id = fields.Many2one('cowin_foundation.cowin_foudation',
    #                                 related='subproject_id.foundation_id', string=u'基金')
    #
    # the_amount_of_financing = fields.Float(
    #     related='subproject_id.the_amount_of_financing', string=u'本次融资额')
    #
    # the_amount_of_investment = fields.Float(
    #     related='subproject_id.the_amount_of_investment', string=u'本次投资金额')
    # ownership_interest = fields.Integer(
    #     related='subproject_id.ownership_interest', string=u'股份比例')
    # ---------------



    round_financing_and_Foundation_ids = fields.One2many('cowin_project.round_financing_and_foundation',
                                                         'sub_invest_decision_committee_res_id',
                                                         string=u'添加基金')


    trustee_id = fields.Many2one('hr.employee', string=u'董事')
    supervisor_id = fields.Many2one('hr.employee', string=u'监事')
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

        res._compute_value() # 写入----> 轮次基金实体
        target_sub_tache_entity.write({
            'res_id': res.id,
            # 'is_unlocked': True,
            'view_or_launch': True,
        })

        # 判断 发起过程 是否需要触发下一个子环节
        # target_sub_tache_entity.check_or_not_next_sub_tache()
        target_sub_tache_entity.update_sub_approval_settings()

        # 来解锁投资决策申请环节新增操作!!!
        meta_sub_project_entity.sub_tache_ids.search([(u'name', u'=', u'投资决策申请')])
        target = meta_sub_project_entity.sub_tache_ids.filtered(lambda sub: sub.name == u'投资决策申请')
        target.write({
            'once_or_more': True,
        })

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
        # target_sub_tache_entity.check_or_not_next_sub_tache()
        target_sub_tache_entity.update_sub_approval_settings()

        return result



    def load_and_return_action(self, **kwargs):
        tache_info = kwargs['tache_info']
        # tache_info = self._context['tache']
        meta_sub_project_id = int(tache_info['meta_sub_project_id'])

        meta_sub_project_entity = self.env['cowin_project.meat_sub_project'].browse(meta_sub_project_id)

        sub_project_entity = meta_sub_project_entity.sub_project_ids[0] # 获取子工程实体

        # tem = meta_sub_project_entity.project_id.copy_data()[0]

        res = {}


        common_fileds = [
            'round_financing_id',
            'foundation_id',
            'the_amount_of_financing',
            'the_amount_of_investment',
            'ownership_interest',
        ]

        tem = meta_sub_project_entity.round_financing_and_Foundation_ids[0].read(common_fileds)[0]
        for k, v in tem.iteritems():
            nk = 'default_' + k
            if type(v) is tuple:
                res[nk] = v[0]
            else:
                res[nk] = v


        # target_fileds = ['name', 'project_number', 'invest_manager_id', 'trustee', 'supervisor']
        target_fileds = ['name', 'project_number', 'invest_manager_id']

        tem = sub_project_entity.read(target_fileds)[0]
        for k, v in tem.iteritems():
            nk = 'default_' + k
            if type(v) is tuple:
                res[nk] = v[0]
            else:
                res[nk] = v



        return {
            'name': self._name,
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'views': [[False, 'form']],
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_id': self.id,
            'target': 'new',
            'context': res,
        }
