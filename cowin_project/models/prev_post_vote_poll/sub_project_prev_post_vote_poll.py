# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import SUPERUSER_ID


class Prev_post_vote_poll(models.Model):
    _inherit = 'ir.needaction_mixin'

    _inherit = 'ir.needaction_mixin'

    _name = 'cowin_project.prev_post_vote_poll'

    '''
        投前/投后会议表决票
    '''

    sub_prev_post_poll_status_id = fields.Many2one('cowin_project.sub_prev_post_poll_status', string=u'投票状态实体', ondelete="cascade")

    name = fields.Char(string=u"项目名称")
    project_number = fields.Char(string=u'项目编号')
    invest_manager_ids = fields.Many2many('hr.employee', 'prev_post_vote_poll_invest_manager_employee_id', string=u'投资经理')

    # # ----------  投资基金

    round_financing_id = fields.Many2one('cowin_common.round_financing', string=u'融资轮次')
    foundation_id = fields.Many2one('cowin_foundation.cowin_foudation', string=u'基金名称')
    the_amount_of_financing = fields.Float(string=u'本次融资金额')
    the_amount_of_investment = fields.Float(string=u'本次投资金额')
    ownership_interest = fields.Integer(string=u'股份比例')

    members_of_voting_committee_ids = fields.Many2many('hr.employee', 'prev_post_vote_poll_members_of_voting_committee_employee_rel', string=u'投决会委员')
    voter = fields.Many2one('hr.employee', string=u'表决人')


    vote_status = fields.Selection([(0, u'初始化'), (1, u'进行中'), (2, u'已完成')], string=u'投票状态', default=0, store=True)


    # 用以判断是投前还是投后的字段
    prev_or_post_vote = fields.Boolean(string=u'投前/投后', default=True)

    # ---> 投前表决使用到的字段
    voting_committee_date = fields.Date(string=u'投决会日期')
    # voting_score = fields.Float(string=u'表决分数')

    # @api.model
    # def _voting_score_inner(self):
    #     res = range(2, 11)
    #     res = map(lambda x: x / 2.0, res)
    #     res = map(lambda x: (str(x), str(x)))
    #     return res

    voting_score = fields.Selection([
        ('1.0', '1.0'),
        ('1.5', '1.5'),
        ('2.0', '2.0'),
        ('2.5', '2.5'),
        ('3.0', '3.0'),
        ('3.5', '3.5'),
        ('4.0', '4.0'),
        ('4.5', '4.5'),
        ('5.0', '5.0'),
    ], string=u'表决分数')


    # voting_score = fields.Selection([(1, '1.0'), (1, '1.5'), (2, '2.0'), (2, '2.5'), (3, '3.0'),
    #                              (3, '3.5'), (4, '4.0'), (4, '4.5'), (5, '5.0')], string=u'表决分数')
    voting_opinion = fields.Text(string=u'表决意见')

    compute_voting_score = fields.Integer(string=u'计算字段', compute='_compute_voting_score')

    @api.depends('voting_score', 'voting_result')
    def _compute_voting_score(self):  # 通过计算字段,来动态的修改
        for rec in self:
            # 投票完成!!!
            rec.vote_status = 2



    # 投后表决使用到的字段
    conference_date = fields.Date(string=u'会议日期')
    voting_result = fields.Selection([(1, u'同意'), (2, u'不同意')], string=u'表决结果')





    @api.multi
    def write(self, vals):
        self.ensure_one()
        # 投票完成状态

        # 投票中,方可进行投票
        if self.vote_status == 1:
            if self.prev_or_post_vote:  # 投前
                voting_score = float(vals.get('voting_score', 0.0))
                self.sub_prev_post_poll_status_id.prev_voting_statistics += voting_score
                self.sub_prev_post_poll_status_id.compute_voting_statistics()
            else:                       # 投后
                voting_result = 1.0 if vals.get('voting_result') == 1 else 0.0
                self.sub_prev_post_poll_status_id.voting_voting_for_true += voting_result
                self.sub_prev_post_poll_status_id.compute_voting_statistics()

            vals['vote_status'] = 2

        res = super(Prev_post_vote_poll, self).write(vals)
        return res


    @api.model
    def _needaction_domain_get(self):
        print(u'使用拦截器的概念的操作模型!!!')

        # 获得 该角色所对应的所有的员工
        if self.env.user.id != SUPERUSER_ID:
            ids = self.env.user.employee_ids.ids
            ids.append(SUPERUSER_ID)
            return [('vote_status', '=', 1), ('voter', '=', self.env.user.employee_ids[0].id)]


        return [('vote_status', '=', 1)]


    def search(self, args, offset=0, limit=None, order=None, count=False):

        if self.env.context.get('custom_filter'):
            if self.env.user.id != SUPERUSER_ID:
            # 后天,自定义数据的操作!!!
                filter = ['voter', '=', self.env.user.employee_ids[0].id]
                args.append(filter)

        res = super(Prev_post_vote_poll, self).search(args, offset, limit, order, count)



        # 把表决人的数据进行拦截操作!!!


        return res