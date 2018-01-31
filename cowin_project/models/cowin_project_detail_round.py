# -*- coding: utf-8 -*-
from odoo import models, fields


class Cowin_project_detail_round(models.Model):

    _name = 'cowin.project.detail.round'

    project_id = fields.Many2one('cowin_project.cowin_project', string='Project', ondelete='restrict')

    round_financing_id = fields.Many2one('cowin_common.round_financing', string=u'融资轮次')

    the_amount_of_financing = fields.Float(string=u'本次融资额')

    project_valuation = fields.Float(string=u'估值')

    foundation_ids = fields.One2many('cowin.project.detail.foundation', 'round_id')

    _sql_constraints = [
        ('cowin_project_detail_round_project_unique', 'unique (project_id, round_financing_id)', u"项目轮次不可重复"),
    ]
