# -*- coding: utf-8 -*-
from odoo import models, fields, api


# 行业model
class Cowin_Common(models.Model):
    _name = 'cowin_common.cowin_industry'

    name = fields.Char(string=u'行业', required=True)

    _sql_constraints = [
        ('industry_key', 'UNIQUE (name)', u'行业名不能相同')
    ]


#项目来源
class Cowin_common_project_source(models.Model):
    _name = 'cowin_common.project_source'

    name = fields.Char(string=u'项目来源', required=True)

    _sql_constraints = [
            ('name_key', 'UNIQUE (name)', u'来源名不能够相同')
        ]


# 轮次model
class Cowin_round_financing(models.Model):
    _name = 'cowin_common.round_financing'

    name = fields.Char(string=u'轮次')

    _sql_constraints = [
            ('name_key', 'UNIQUE (name)', u'轮次名不能够相同')
        ]



# 审批角色
class Cowin_common_approval_role(models.Model):

    _name = 'cowin_common.approval_role'

    '''
        审批角色
    '''


    name = fields.Char(string=u'角色名')

    # user_ids = fields.Many2many('res.users', string=u'用户')

    _sql_constraints = [
        ('name_key', 'UNIQUE (name)', u'审批角色名称不能相同!!!'),
    ]


