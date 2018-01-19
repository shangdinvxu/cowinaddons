# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class Prev_poll_status(models.Model):
    _name = 'cowin_project.sub_prev_post_poll_status'

    '''
        投前/投后投资决策委员会会议表决结果
    '''
    subproject_id = fields.Many2one('cowin_project.cowin_subproject', string=u'子工程实体', ondelete="cascade")
    sub_tache_id = fields.Many2one('cowin_project.subproject_process_tache', string=u'子环节实体')


    name = fields.Char(string=u"项目名称")
    project_number = fields.Char(string=u'项目编号')

    prev_voting_statistics = fields.Float(string=u'投前投票统计')
    post_voting_statistics = fields.Float(string=u'投后投票统计')

    voting_result = fields.Char(string=u'投票结果')
    # 用以判断是投前还是投后的字段
    prev_or_post_vote = fields.Boolean(string=u'投前/投后', default=True)

    # compute_voting_count = fields.Integer(compute='_compute_voting_statistics', store=True, default=0)
    compute_voting_count = fields.Integer(default=0, string=u'投票记录')
    voting_voting_for_true = fields.Integer(default=0, string=u'同意的个数')


    @api.multi
    def compute_voting_statistics(self):
        self.ensure_one()
        if self.voting_status == 2 or self.voting_status == 3:
            return

        self.compute_voting_count += 1

        if self.prev_or_post_vote:
            if self.compute_voting_count == len(self.sudo().prev_post_conference_resolutions_ids):  # 这个是非常大意的地方,权限的问题,让代码变得走不下去!!!
                tmp = self.prev_voting_statistics = self.prev_voting_statistics / len(self.sudo().prev_post_conference_resolutions_ids)
                # self.voting_statistics  = tmp * 100
                low, high = self.get_rating_from_the_amount_of_investment()
                if tmp >= low and tmp <= high:
                    # 触发下一个子环节
                    # self.voting_status = 2
                    # self.voting_result = u'同意'

                    # self.sub_tache_id.sub_pro_approval_flow_settings_ids.upate_status(4)

                    self.write({
                        'voting_status': 2,
                        'voting_result': u'同意',
                    })
                else:
                    # 拒绝,不能继续往下面走
                    # self.voting_status = 3
                    # self.voting_result = u'拒绝'

                    self.write({
                        'voting_status': 3,
                        'voting_result': u'拒绝',
                    })
                    # self.sub_tache_id.sub_pro_approval_flow_settings_ids.upate_status(5)

            else:
                self.voting_result = u'还有%s人,没有投票' % (len(self.sudo().prev_post_conference_resolutions_ids) - self.compute_voting_count)


        else:
            # 投后状态
            tmp = 1.0 / len(self.sudo().prev_post_conference_resolutions_ids)
            tmp = tmp * self.compute_voting_count
            self.post_voting_statistics = tmp * 100
            if self.compute_voting_count == len(self.sudo().prev_post_conference_resolutions_ids):

                if tmp >= 2.0 / 3:
                    # 触发下一个子环节
                    # self.voting_status = 2
                    # self.voting_result = u'同意'
                    self.write({
                        'voting_status': 2,
                        'voting_result': u'同意',
                    })
                    # self.sub_tache_id.sub_pro_approval_flow_settings_ids.upate_status(4)
                else:
                    # 拒绝,不能继续往下面走
                    # self.voting_status = 3
                    # self.voting_result = u'拒绝'

                    self.write({
                        'voting_status': 3,
                        'voting_result': u'拒绝',
                    })
                    # self.sub_tache_id.sub_pro_approval_flow_settings_ids.upate_status(5)

            else:
                self.voting_result = u'还有%s人,没有投票' % (len(self.sudo().prev_post_conference_resolutions_ids) - self.compute_voting_count)






    # voting_status = fields.Boolean(string=u'是否完成')
    voting_status = fields.Selection([(0, u'初始化'), (1, u'投票中'), (2, u'已完成'), (3, u'拒绝')], string=u'投票状态', default=0, store=True)


    prev_post_conference_resolutions_ids = fields.One2many('cowin_project.prev_post_vote_poll', 'sub_prev_post_poll_status_id', string=u'投前/投后会议决票实体')

    # ----------  投资基金
    round_financing_id = fields.Many2one('cowin_common.round_financing', string=u'融资轮次')
    foundation_id = fields.Many2one('cowin_foundation.cowin_foudation', string=u'基金名称')
    the_amount_of_financing = fields.Float(string=u'本次融资金额')
    the_amount_of_investment = fields.Float(string=u'本次投资金额')
    ownership_interest = fields.Integer(string=u'股份比例')
    # ----------


    def get_rating_from_the_amount_of_investment(self):

        if self.the_amount_of_investment <= 1000 * 10000 and self.the_amount_of_investment > 0:
            return (3.0, 5.0)

        elif self.the_amount_of_investment > 1000 * 10000 and self.the_amount_of_investment <= 3000 * 10000:
            return (4.0, 5.0)

        else:
            return (4.5, 5.0)



    # @api.model
    # def create(self, vals):
    #     tache_info = self._context['tache']
    #
    #     # sub_project_id = int(tache_info['sub_project_id'])
    #
    #     sub_tache_id = int(tache_info['sub_tache_id'])
    #     meta_sub_project_id = int(tache_info['meta_sub_project_id'])
    #     meta_sub_project_entity = self.env['cowin_project.meat_sub_project'].browse(meta_sub_project_id)
    #
    #     sub_project_id = meta_sub_project_entity.sub_project_ids.id
    #
    #     target_sub_tache_entity = meta_sub_project_entity.sub_tache_ids.browse(sub_tache_id)
    #
    #     vals['subproject_id'] = sub_project_id
    #     res = super(Prev_poll_status, self).create(vals)
    #     target_sub_tache_entity.write({
    #         'res_id': res.id,
    #         # 'is_unlocked': True,
    #         'view_or_launch': True,
    #     })
    #
    #     #判断 发起过程 是否需要触发下一个子环节
    #     target_sub_tache_entity.check_or_not_next_sub_tache()
    #     target_sub_tache_entity.update_sub_approval_settings()
    #
    #     #触发下一个依赖子环节处于解锁状态
    #     for current_sub_tache_entity in meta_sub_project_entity.sub_tache_ids:
    #         if current_sub_tache_entity.parent_id == target_sub_tache_entity:
    #             current_sub_tache_entity.write({
    #                 'is_unlocked': True,
    #             })
    #
    #     return res




    @api.multi
    def write(self, vals):
        res = super(Prev_poll_status, self).write(vals)

        # 由于在投票状态之中,是通过compute计算字段做操作,所以 context中并不会传递tache数据
        # 但是数据已经保存在了子环节中
        # sub_tache_e = self.subproject_id.meta_sub_project_id.sub_tache_ids.filtered(
        #     lambda sub_tache: sub_tache.tache_id.model_id.model_name == self._name and sub_tache.res_id == self.id)


        target_sub_tache_entity = self.sub_tache_id

        # 投票完成
        if self.voting_status == 2:
            target_sub_tache_entity.write({
                'is_launch_again': False,
            })

            # 判断 发起过程 是触发下一个子环节
            # target_sub_tache_entity.check_or_not_next_sub_tache()
            # target_sub_tache_entity.trigger_next_subtache()
            self.sub_tache_id.sub_pro_approval_flow_settings_ids.upate_status(7)

        elif self.voting_status == 3:
            # 不需要再做从新发起的状态!!!
            target_sub_tache_entity.sub_pro_approval_flow_settings_ids.set_reject()


        return res

    def load_and_return_action(self, **kwargs):
        tache_info = kwargs['tache_info']
        # tache_info = self._context['tache']
        meta_sub_project_id = int(tache_info['meta_sub_project_id'])

        meta_sub_project_entity = self.env['cowin_project.meat_sub_project'].browse(meta_sub_project_id)

        sub_project_entity = meta_sub_project_entity.sub_project_ids[0]  # 获取子工程实体

        # tem = meta_sub_project_entity.project_id.copy_data()[0]

        common_fileds = [
            'round_financing_id',
            'foundation_id',
            'the_amount_of_financing',
            'the_amount_of_investment',
            'ownership_interest',
        ]

        common_fileds.extend(['name', 'project_number'])

        # tem = sub_project_entity.read(common_fileds)[0]
        tem = meta_sub_project_entity.round_financing_and_Foundation_ids[0].read(common_fileds)[0]


        res = {}

        for k, v in tem.iteritems():
            nk = 'default_' + k
            if type(v) is tuple:
                res[nk] = v[0]
            else:
                res[nk] = v

        # 默认的投资经理的数据我们需要去自定义添加
        invest_manager_entity = self.env['cowin_common.approval_role'].search([('name', '=', u'投资经理')])
        rel_entities = meta_sub_project_entity.sub_meta_pro_approval_settings_role_rel & invest_manager_entity.sub_meta_pro_approval_settings_role_rel

        res['default_invest_manager_ids'] = [(6, 0, [rel.employee_id.id for rel in rel_entities])]

        investment_decision_committee_entity = self.env['cowin_common.approval_role'].search([('name', '=', u'投资决策委员')])
        rel_entities = meta_sub_project_entity.sub_meta_pro_approval_settings_role_rel & investment_decision_committee_entity.sub_meta_pro_approval_settings_role_rel
        res['default_members_of_voting_committee_ids'] = [(6, 0, [rel.employee_id.id for rel in rel_entities])]


        # 默认情况下 一对一
        res['default_voter_id'] = self.env.user.employee_ids[0].id
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




