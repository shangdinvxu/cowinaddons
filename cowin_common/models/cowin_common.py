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

    _sql_constraints = [
            ('name_key', 'UNIQUE (name)', u'轮次名不能够相同')
        ]



