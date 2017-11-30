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

    sub_approval_flow_settings_ids = fields.One2many('cowin_project.sub_approval_flow_settings', 'meta_sub_project_id',
                                                     string=u'子流程配置实例')






    @api.model
    def create(self, vals, **kwargs):

        meta_sub_project = super(Meat_sub_project, self).create(vals)

        project_id = vals['project_id']

        project_entity = self.env['cowin_project.cowin_project'].browse(project_id)

        project_settings_entity = project_entity.process_id



        for tache_entity in project_settings_entity.get_all_tache_entities():
            if tache_entity.model_id.model_name == project_entity._name:
                continue

            # 1 创建子环节实体, 并且对自环节实体进行环节依赖的设定
            # self.env['cowin_project.subproject_process_tache'].create({


            meta_sub_project.sub_tache_ids.create({
                'tache_id': tache_entity.id,
                'meta_sub_project_id': meta_sub_project.id,
            })


            # 2 创建子流程配置实体
            meta_sub_project.sub_approval_flow_settings_ids.create({
                'meta_sub_project_id': meta_sub_project.id,
                # 理论上主环节中只有一份主审批流实体
                'approval_flow_settings_id': tache_entity.approval_flow_settings_ids.id,
                # 默认就指向第一个位置!!!
                'current_approval_flow_node_id': tache_entity.approval_flow_settings_ids.approval_flow_setting_node_ids[0].id,
            })


        # 要对子环节设定依赖
        base_tache_entity = [tache_entity for tache_entity in project_settings_entity.get_all_tache_entities()
                             if tache_entity.model_id.model_name == project_entity._name
                             ][0]

        for sub_tache_entity in meta_sub_project.sub_tache_ids:

            # 拿到主环节实体
            tache_entity = sub_tache_entity.tache_id

            # 激活子工程发起项目!!!
            if tache_entity.model_id.model_name == meta_sub_project.sub_project_ids._name:
                sub_tache_entity.write({
                    'is_unlocked': True,
                })

                # 改变当前子环节所对应的子审批流的配置

                target_sub_approval_flow_entity = sub_tache_entity.tache_id.approval_flow_settings_ids.sub_approval_flow_settings_ids & \
                                                  meta_sub_project.sub_approval_flow_settings_ids

                target_sub_approval_flow_entity.write({
                    'status': 2,
                })



            # 主环节依赖的实体
            parent_tache_entity = tache_entity.parent_id

            # 过滤主工程 主环节实体
            if parent_tache_entity == base_tache_entity:
                continue


            # 获取主依赖环节实体中的所有的子环节实体,并且与元子工程实体做 交 的操作


            target_sub_tache_entity = parent_tache_entity.tache_status_id & meta_sub_project.sub_tache_ids

            # 写入依赖条件
            sub_tache_entity.write({
                'parent_id': target_sub_tache_entity.id
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