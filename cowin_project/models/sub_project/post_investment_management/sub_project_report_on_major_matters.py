# -*- coding: utf-8 -*-
from odoo import models, fields, api


class sub_project_report_on_major_matters(models.Model):

    _name = 'cowin_project.sub_report_on_major_matters'


    '''
        重大事项报告
    '''

    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')

    a = fields.Many2one('报告人', string=u'报告人')

    b = fields.Datetime(string=u'提交日期')

    c = fields.Char(string=u'事项关键词', required=True)

    d = fields.Text(string=u' 事项内容', required=True)

    e = fields.Text(string=u'重大影响', required=True)

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