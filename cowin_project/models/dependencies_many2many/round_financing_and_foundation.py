# -*- coding: utf-8 -*-
from odoo import models, fields, api



# 轮次model
class Cowin_round_financing_inherit(models.Model):
    _inherit = 'cowin_common.round_financing'

    '''
            轮次
    '''

    round_financing_for_foundation_ids = fields.One2many('cowin_project.round_financing_and_foundation',
                                                         'round_financing_id'
                                                         )


class Cowin_foundation_inherit(models.Model):
    _inherit = 'cowin_foundation.cowin_foudation'

    '''
           基金
    '''

    foundation_for_rund_financing_ids = fields.One2many('cowin_project.round_financing_and_foundation', 'foundation_id', string=u'基金轮次')



# 轮次基金 subproject  model
class Round_financing_and_Foundation(models.Model):
    _name = 'cowin_project.round_financing_and_foundation'


    name = fields.Char(string=u'轮次基金表')
    # sub_project_id = fields.Many2one('cowin_project.cowin_sub_project', string=u'子工程')
    meta_sub_project_id = fields.Many2one('cowin_project.meat_sub_project', string=u'元子工程实例',
                                          ondelete="cascade")

    #   ---- 投资决策会议实例
    sub_invest_decision_committee_res_id = fields.Many2one('cowin_project.sub_invest_decision_committee_res',
                                                           string=u'投资决策会议实例')

    round_financing_id = fields.Many2one('cowin_common.round_financing', string=u'融资轮次')

    foundation_id = fields.Many2one('cowin_foundation.cowin_foudation', string=u'基金')

    stage = fields.Selection([(1, u'registed'), (2, u'finish')], string=u'状态', default=1)