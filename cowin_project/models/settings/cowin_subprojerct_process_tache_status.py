# -*- coding: utf-8 -*-
from odoo import models, fields, api
import itertools
from odoo.exceptions import UserError


class Cowin_subprojerct_prcess_tache_status(models.Model):
    _name = 'cowin_project.subproject_process_tache'


    '''
        每个子subproject都有自己的环节状态信息
    '''


    name = fields.Char(string=u'环节名')

    tache_id = fields.Many2one('cowin_project.process_tache', string=u'环节', ondelete="restrict")

    parent_id = fields.Many2one('cowin_project.subproject_process_tache')

    # 排序链表
    order_parent_id = fields.Many2one(_name, string=u'排序链表')

    # sub_project_id  = fields.Many2one('cowin_project.cowin_subproject', string=u'字工程名')
    meta_sub_project_id = fields.Many2one('cowin_project.meat_sub_project', string=u'元子工程实例', ondelete="cascade")

    # 这三条数据对应的是不同的子工程的使用,其他数据不会变更
    is_unlocked = fields.Boolean(string=u'是否已解锁', default=False)
    # is_unlocked = fields.Selection([(0, u'未解锁'), (1, u'解锁中'), (2, u'已解锁')], string=u'解锁条件', default=0)
    res_id = fields.Integer(string=u'该环节对应该实例另一个字段model_id中的一个实例')
    view_or_launch = fields.Boolean(string=u'发起或者创建', default=False)

    once_or_more = fields.Boolean(string=u'是否发起多次', default=False)
    sub_pro_approval_flow_settings_ids = fields.One2many('cowin_project.sub_approval_flow_settings', 'sub_project_tache_id', string=u'子审批实体')

    order = fields.Integer()

    index = fields.Integer(string=u'多个自定义的环节', default=0)


    is_launch_again = fields.Boolean(string=u'是否重新发起', default=False)



    @api.model
    def create(self, vals):
        # 在子审批流中创建子审批审批实体和自审批通道!!!
        res = super(Cowin_subprojerct_prcess_tache_status, self).create(vals)

        # 1 创建子流程配置实体
        res2 = res.sub_pro_approval_flow_settings_ids.create({
            'sub_project_tache_id': res.id,
            'meta_sub_project_id': res.meta_sub_project_id.id,
            # 理论上主环节中只有一份主审批流实体
            'approval_flow_settings_id': res.tache_id.approval_flow_settings_ids.id,
            # 默认就指向第一个位置!!!
            'current_approval_flow_node_id': res.tache_id.approval_flow_settings_ids.approval_flow_setting_node_ids.sorted('order')[0].id,
        })

        # # 每个子审批节点创建一条通道
        # channel_entity = self.env['mail.channel'].create({
        #     'name': u'子审批通道:%s' % res2.id,
        #     "public": "public",
        # })
        #
        # # 写入通道数据
        # res2.write({
        #     'channel_id': channel_entity.id,
        # })

        return res





    def get_tache(self):
        return self.tache_id

    # 投资决策委员会会议表决票 有特殊的操作,业务有关联
    # 而且,投前/投后 通过prev_or_post_vote 来区分 prev_or_post_vote = True 代表投前
    def write_special_vote(self, prev_or_post_vote=True):
        for sub_tache_entity in self.meta_sub_project_id.sub_tache_ids:
            # 这个操作只会去触发可能有多个子环节的解锁,如果解锁则不需要再次解锁
            if sub_tache_entity.order_parent_id == self and not sub_tache_entity.is_unlocked:

                name = self.meta_sub_project_id.sub_project_ids[0].name
                project_number = self.meta_sub_project_id.sub_project_ids[0].project_number
                voting_committee_date = self.meta_sub_project_id.sub_project_ids[0].voting_committee_date


                meta_sub_project_entity = self.meta_sub_project_id
                # 默认的投资经理的数据我们需要去自定义添加
                vals = {
                    'name': name,
                    'project_number': project_number,
                    'voting_committee_date': voting_committee_date,
                }

                res = {}
                # res 目的在于把之前保存在轮次基金实体中的数据取出来,以供投票状态的使用操作!!!
                common_fileds = [
                    'round_financing_id',
                    'foundation_id',
                    'the_amount_of_financing',
                    'the_amount_of_investment',
                    'ownership_interest',
                ]

                # res = meta_sub_project_entity.round_financing_and_Foundation_ids[0].read(common_fileds)[0]

                # res.update(vals)

                tem = meta_sub_project_entity.round_financing_and_Foundation_ids[0].read(common_fileds)[0]
                for k, v in tem.iteritems():
                    nk = k
                    if type(v) is tuple:
                        res[nk] = v[0]
                    else:
                        res[nk] = v



                invest_manager_entity = self.env['cowin_common.approval_role'].search([('name', '=', u'投资经理')])
                rel_entities = meta_sub_project_entity.sub_meta_pro_approval_settings_role_rel & invest_manager_entity.sub_meta_pro_approval_settings_role_rel

                # vals['default_invest_manager_ids'] = [(6, 0, [rel.employee_id.id for rel in rel_entities])]
                res['invest_manager_ids'] = vals['invest_manager_ids'] = [(6, 0, [rel.employee_id.id for rel in rel_entities])]

                investment_decision_committee_entity = self.env['cowin_common.approval_role'].search([('name', '=', u'投资决策委员')])
                rel_entities = meta_sub_project_entity.sub_meta_pro_approval_settings_role_rel & investment_decision_committee_entity.sub_meta_pro_approval_settings_role_rel
                c_entity_rels = rel_entities

                res['members_of_voting_committee_ids'] = vals['members_of_voting_committee_ids'] = [(6, 0, [rel.employee_id.id for rel in rel_entities])]

                # 创建投票状态实体
                model_name = sub_tache_entity.tache_id.model_id.model_name
                e = self.env[model_name].create(res)

                # 写入依赖的外键操作!!!
                e.write({
                    'subproject_id': meta_sub_project_entity.sub_project_ids[0].id,
                    'prev_or_post_vote': prev_or_post_vote,
                })



                # 解锁该子环节
                sub_tache_entity.write({
                    'is_unlocked': True,
                    'res_id': e.id,
                    'view_or_launch': True,
                })

                # 同时不再考虑该子环节中审批节点的问题
                sub_tache_entity.sub_pro_approval_flow_settings_ids[0].write({
                    'status': 4,
                    'prev_status': 4,
                })



                # 创建投票实体  投决会日期
                vals['voting_committee'] = meta_sub_project_entity.sub_project_ids[0].voting_committee
                vals['sub_prev_post_poll_status_id'] = e.id
                vals['prev_or_post_vote'] = prev_or_post_vote

                # 初始化 各个投票实体
                for rel_entity in c_entity_rels:
                    poll_entity = e.prev_post_conference_resolutions_ids.create(vals)
                    poll_entity.write({
                        'voter': rel_entity.employee_id.id,

                    })


                #修改 投票状态实体 为投票状态
                e.write({
                    'voting_status': 1,
                    'voting_result': u'还有%s人,没有投票' % (len(e.prev_post_conference_resolutions_ids)),
                })


                # 修改 投票实体  为投票状态
                for poll_entity in e.prev_post_conference_resolutions_ids:
                    poll_entity.write({
                        'vote_status': 1,
                    })





                # 提前把需要生成的



                # sub_tache_entity.sub_pro_approval_flow_settings_ids.write({
                #     'status': 4,
                # })




    def update_sub_approval_settings(self):  # 调用子审批流实体
        self.sub_pro_approval_flow_settings_ids.upate_status(2)

    def trigger_next_subtache(self): # 只触发解锁条件
        for sub_tache_entity in self.meta_sub_project_id.sub_tache_ids:
            # 这个操作只会去触发可能有多个子环节的解锁,如果解锁则不需要再次解锁
            if sub_tache_entity.parent_id == self and not sub_tache_entity.is_unlocked:
                sub_tache_entity.write({
                    'is_unlocked': True,
                })




    # def check_or_not_next_sub_tache(self):
    #     if self.sub_pro_approval_flow_settings_ids.update_final_approval_flow_settings_status_and_node():
    #         # 当前子审批实体状态设置为4
    #         # self.sub_pro_approval_flow_settings_ids.status = 4
    #         # self.sub_pro_approval_flow_settings_ids.write({
    #         #         'status': 4,
    #         #     })
    #
    #         # self.sub_pro_approval_flow_settings_ids.update_final_approval_flow_settings_status_and_node()
    #         for sub_tache_entity in self.meta_sub_project_id.sub_tache_ids:
    #             # 这个操作只会去触发下一个子环节的解锁,如果解锁则不需要再次解锁
    #             if sub_tache_entity.parent_id == self and not sub_tache_entity.is_unlocked:
    #                                 sub_tache_entity.write({
    #                                     'is_unlocked': True,
    #                                     })
    #
    #                                 # 触发下面的所有的依赖于该环节的解锁!!!
    #                                 # break
    #
    #     else:
    #         # 调整审核状态
    #
    #         # 更新子审批实体的状态
    #         self.sub_pro_approval_flow_settings_ids.update_approval_flow_settings_status_and_node()



    # 重新设定依赖写入的问题
    # def set_depency_order_by_sub_tache(self):
    #
    #     # 找到主工程的环节
    #
    #     # if len(self) > 1:
    #     #     this = self[0]
    #
    #     this = self[0] if len(self) > 1 else self
    #
    #     base_tache_entity = [tache_entity for tache_entity in this.meta_sub_project_id.project_id.process_id.get_all_tache_entities()
    #                          if tache_entity.model_id.model_name == this.meta_sub_project_id.project_id._name
    #                          ][0]
    #
    #
    #     count = itertools.count(1)
    #     base_sub_tache_entity = [entity for entity in this.meta_sub_project_id.sub_tache_ids \
    #                                                         if entity.tache_id.parent_id == base_tache_entity][0]
    #     base_sub_tache_entity.write({
    #         'order': count.next(),
    #     })
    #
    #     current_sub_tache_entity = base_sub_tache_entity
    #
    #     a = set()
    #     while current_sub_tache_entity:
    #         if current_sub_tache_entity in a:
    #             break
    #
    #         for sub_tache_entity in this.meta_sub_project_id.sub_tache_ids:
    #             if sub_tache_entity == current_sub_tache_entity:
    #                 a.add(sub_tache_entity)
    #                 continue
    #             if sub_tache_entity.parent_id == current_sub_tache_entity:
    #                 a.add(current_sub_tache_entity)
    #                 sub_tache_entity.write({'order': count.next()})
    #                 current_sub_tache_entity = sub_tache_entity
    #
    #
    #
    #     return 'kk'