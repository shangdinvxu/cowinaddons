# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Prev_post_vote_poll(models.Model):

    _name = 'cowin_project.prev_post_vote_poll'

    '''
        投前/投后会议表决票
    '''

    sub_prev_post_poll_status_id = fields.Many2one('cowin_project.sub_prev_post_poll_status', string=u'投票状态实体', ondelete="cascade")

    name = fields.Char(string=u"项目名称")
    project_number = fields.Char(string=u'项目编号')
    invest_manager_ids = fields.Many2many('hr.employee', string=u'投资经理')

    # ----------  投资基金

    round_financing_id = fields.Many2one('cowin_common.round_financing', string=u'融资轮次')
    foundation_id = fields.Many2one('cowin_foundation.cowin_foudation', string=u'基金名称')
    the_amount_of_financing = fields.Float(string=u'本次融资金额')
    the_amount_of_investment = fields.Float(string=u'本次投资金额')
    ownership_interest = fields.Integer(string=u'股份比例')

    members_of_voting_committee_ids = fields.Many2many('hr.employee', string=u'投决会委员')
    voter = fields.Many2one('hr.employee', string=u'表决人')


    vote_status = fields.Selection([(1, u'进行中'), (2, u'已完成')], string=u'投票状态', default=1)


    # 用以判断是投前还是投后的字段
    prev_or_post_vote = fields.Boolean(string=u'投前/投后', default=True)

    # ---> 投前表决使用到的字段
    voting_committee = fields.Date(string=u'投决会日期')
    voting_score = fields.Float(string=u'表决分数')
    voting_opinion = fields.Text(string=u'表决意见')



    # 投后表决使用到的字段
    conference_date = fields.Date(string=u'会议日期')
    voting_result = fields.Boolean(string=u'表决结果')









    def search(self, args, offset=0, limit=None, order=None, count=False):
        print(u'..... ---->   context is %s' % self._context.get(u'vote_status'))
        return super(Prev_post_vote_poll, self).search(args, offset, limit, order, count)

