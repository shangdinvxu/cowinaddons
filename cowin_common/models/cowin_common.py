# -*- coding: utf-8 -*-
from odoo import models, fields, api


# 行业model
class Cowin_Common(models.Model):
    _name = 'cowin_common.cowin_industry'

    name = fields.Char(string=u'行业', required=True)

    _sql_constraints = [
        ('industry_key', 'UNIQUE (name)', u'行业名不能相同')
    ]


# 轮次model
class Cowin_round_financing(models.Model):
    _name = 'cowin_common.round_financing'

    name = fields.Char(string=u'轮次')

    round_financing_for_foundation_ids = fields.One2many('cowin_project.round_financing_and_foundation',
                                                         'round_financing_id'
                                                         )


    _sql_constraints = [
            ('name_key', 'UNIQUE (name)', u'轮次名不能够相同')
        ]



# 轮次基金 subproject  model
class Round_financing_and_Foundation(models.Model):
    _name = 'cowin_project.round_financing_and_foundation'


    name = fields.Char(string=u'阶段表')
    sub_project_id = fields.Many2one('cowin_project.cowin_sub_project', string=u'子工程')

    round_financing_id = fields.Many2one('cowin_common.round_financing', string=u'融资轮次')

    foundation_id = fields.Many2one('cowin_foundation.cowin_foudation', string=u'基金')

    stage = fields.Selection([(1, u'registed'), (2, u'finish')], string=u'状态', default=1)

