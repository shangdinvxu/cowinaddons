# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Cowin_foundation(models.Model):
    _name = 'cowin_foundation.cowin_foudation'

    name = fields.Char(string=u'基金名称')




    foundation_for_rund_financing_ids = fields.One2many('cowin_project.round_financing_and_foundation', 'foundation_id', string=u'基金轮次')

    _sql_constraints = [
        ('name_key', 'UNIQUE (name)', u'基金名不能够相同')
    ]

    # 得到该基金的某个阶段的实例(记录)
    def get_round_financing(self, round_financing):
        '''

        :param round_financing:  融资轮次
        :return:
        '''
        for stage in self.foudation_stages:
            if stage.round_financing == round_financing:
                return stage

    # 获取该基金在该项目中的各个基金的投资的状态
    def get_all_stage(self):

        return [stage for stage in self.foudation_stages]


