# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Cowin_foudation(models.Model):
    _name = 'cowin_project.cowin_foudation'


    name = fields.Char(string=u'基金名称')

    project_id = fields.Many2one('cowin_project.cowin_project', string=u'项目')

    foudation_stages = fields.One2many('cowin_project.cowin_foudation_stage', 'foudation_id', string=u'基金的各个状态')

    ownership_interest = fields.Float(string=u'股份比例')


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
        res = []
        for stage in self.foudation_stages:
            res.append({
                'id': stage.id,
                'round_financing': stage.round_financing  # 融资轮次
            })

        return {
            'id': self.id,
            'foudation_stages': res
        }





class Cowin_foudation_stage(models.Model):
    _name = 'cowin_project.cowin_foudation_stage'
    foudation_id = fields.Many2one('cowin_project.cowin_foudation', string=u'基金名称', ondelete="cascade")

    investment_amount = fields.Float(string=u'本次投资金额')

    round_financing = fields.Many2one('cowin_project.round_financing', string=u'融资轮次')