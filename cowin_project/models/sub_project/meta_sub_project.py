# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Meat_sub_project(models.Model):
    _name = 'cowin_project.meat_sub_project'

    '''
        元子工程
    '''

    # 主工程信息
    project_id = fields.Many2one('cowin_project.cowin_project', ondelete="cascade")

    # 轮次基金表
    # 理论上只有第一个实例是我们需要运用到
    # round_financing_and_Foundation = fields.Many2one('cowin_project.round_financing_and_foundation', string=u'轮次实例')

    # 第一个实体代表着该元子工程所需要的实体
    # 其他实例代表着在投决会中获得到的实体
    round_financing_and_Foundation_ids = fields.One2many('cowin_project.round_financing_and_foundation', 'meta_sub_project_id',
                                                     string=u'多个轮次基金实例')



    # 理论上只会有一个实例
    sub_project_ids = fields.One2many('cowin_project.cowin_subproject', 'meta_sub_project_id', string=u'子工程实例')


    sub_tache_ids = fields.One2many('cowin_project.subproject_process_tache', 'meta_sub_project_id', string=u'子环节实例')






    @api.model
    def create(self, vals, **kwargs):

        meta_sub_project = super(Meat_sub_project, self).create(vals)

        project_id = vals['project_id']

        project = self.env['cowin_project.cowin_project'].browse(project_id)

        project_settings = project.process_id

        for tache in project_settings.get_all_tache_entities():
            if tache.model_id.model_name == project._name:
                continue

            # 创建子环节实体
            self.env['cowin_project.subproject_process_tache'].create({
                'tache_id': tache.id,
                'meta_sub_project_id': meta_sub_project.id,
            })



        return meta_sub_project



    def get_round_financing_and_foundation(self):

        return self.round_financing_and_Foundation_ids


    def get_target_financing_and_foundation(self):

        # 两种情况  1  工程刚开开始什么都没有的情况下

        #          2   由一个子工程创建出来的情况


        # for r in self.get_round_financing_and_foundation():
        #     # 看来在odoo之中, 关于外键的引用是运用了假实例的布局
        #     if not r.sub_invest_decision_committee_res_id:
        #         return r
        #

        # 这种情况下是最为正确的抉择!!!
        return self.round_financing_and_Foundation_ids[0]




    # # 得到所有的子环节信息
    def get_sub_taches(self):

        return self.sub_tache_ids