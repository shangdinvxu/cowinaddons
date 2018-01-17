# -*- coding: utf-8 -*-
from odoo import models, fields, api
import json
from odoo.tools.mail import html_sanitize, html2plaintext
import time

from odoo import SUPERUSER_ID
class Cowin_sub_project_approval_flow_settings(models.Model):
    _inherit = ['mail.thread']

    _name = 'cowin_project.sub_approval_flow_settings'

    '''
        每个子工程都会有自己的审批流的,所以需要保存属于自己的审批流程的节点的信息
    '''


    name = fields.Char(string=u'子工程审批流节点信息')

    # tache_id = fields.Many2one('cowin_project.process_tache', string=u'环节')
    approval_flow_settings_id = fields.Many2one('cowin_project.approval_flow_settings', string=u'工程审批流', ondelete="restrict")
    meta_sub_project_id = fields.Many2one('cowin_project.meat_sub_project', string=u'元子工程实例', ondelete="cascade")

    status = fields.Selection([(1, u'发起'), (2, u'审核中'), (3, u'暂缓(从新发起)'), (4, u'同意'), (5, u'拒绝'), (6, u'投票中'), (7, u'同意')],
                     string=u'审核状态', default=1)
    prev_status = fields.Integer(default=1)

    # 通道使用,发送通知消息
    # channel_id = fields.Many2one('mail.channel', string=u'发送消息通知的通道')

    action = {(1, 2): u'发起', (2, 2): u'审核', (2, 3): u'暂缓', (1, 4): u'同意', (2, 4): u'同意', (2, 5): u'拒绝',
              (6, 7): u'投票同意', (6, 5): u'投票拒绝'}

    # is_putoff = fields.Boolean(string=u'是否暂缓', default=True)


    # status_trigger = fields.Integer(compute='_compute_status')


    # 用以记录当前的审批节点的位置

    current_approval_flow_node_id = fields.Many2one('cowin_project.approval_flow_setting_node',
                                                                    string=u'当前的审批节点所在的位置!!!')



    sub_pro_approval_flow_settings_record_ids = fields.One2many('cowin_project.sub_approval_flow_settings_record',
                                                                'sub_approval_settings_id', string=u'审批记录')

    # 构建子环节和子审批实体一对一的关系
    sub_project_tache_id = fields.Many2one('cowin_project.subproject_process_tache', string=u'子环节实体')


    def get_all_message(self):
        message_entities = self.env['mail.message'].search([('subject', '=', 'approval_flow_setting'), ('res_id', '=', self.id), ('model', '=', self._name)])
        message_infos = message_entities.mapped(lambda m: html2plaintext(m.body))

        return message_infos



    def send_next_approval_flow_settings_node_msg(self, status=2):
        sub_project_name = self.meta_sub_project_id.sub_project_ids[0].name
        round_financing_name = self.meta_sub_project_id.round_financing_and_Foundation_ids[0].round_financing_id.name
        foundation_name = self.meta_sub_project_id.round_financing_and_Foundation_ids[0].foundation_id.name

        sub_project_name = sub_project_name if sub_project_name else u''
        round_financing_name = round_financing_name if round_financing_name else u'暂无轮次'
        foundation_name = foundation_name if foundation_name else u'暂无基金'

        prev = self.current_approval_flow_node_id
        next = self.current_approval_flow_node_id.parent_id

        # approval_role_name = self.current_approval_flow_node_id.operation_role_id.name
        approval_role_name = next.operation_role_id.name


        info_first = u'%s/%s/%s\n' % (sub_project_name, round_financing_name, foundation_name)

        tmp2 = {}
        tmp2[u'sub_project_name'] = sub_project_name
        tmp2[u'round_financing_name'] = round_financing_name
        tmp2[u'foundation_name'] = foundation_name
        tmp2[u'approval_role_name'] = approval_role_name
        # tmp2[u'approval_roel_person'] = approval_roel_person
        tmp2[u'operation_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 8 * 3600))
        tmp2[u'operation'] = u''
        tmp2[u'sub_tache_name'] = self.sub_project_tache_id.name

        info = u''

        if status == 2: # 待审批
            tmp2[u'operation'] = u'待审批'

            info = info_first + u'您有一项[%s] 待处理' % self.sub_project_tache_id.name

        elif status == 3:
            info = info_first + u'您发起的[%s] 已暂缓' % self.sub_project_tache_id.name
        elif status == 4:
            info = info_first + u'您发起的[%s] 已审批通过' % self.sub_project_tache_id.name
        elif status == 5:
            info = info_first + u'您发起的[%s] 已拒绝' % self.sub_project_tache_id.name

        else:
            tmp2[u'operation'] = u''

        approval_roles = next.operation_role_id

        # 或得到当前的用户
        rel_entities = self.meta_sub_project_id.sub_meta_pro_approval_settings_role_rel & approval_roles.sub_meta_pro_approval_settings_role_rel

        partner_ids = list(map(lambda rel: rel.employee_id.user_id.partner_id.id, rel_entities))
        id = self.env['res.users'].search([('id', '=', 1)]).partner_id.id
        partner_ids.append(id)

        self.current_approval_flow_node_id = prev

        channel_entity = self.env.ref('cowin_project.init_project_mail_channel')

        channel_entity.write({
            'channel_partner_ids': [(4, partner_id) for partner_id in partner_ids],
        })

        # self.channel_id.write({
        #     'channel_partner_ids': [(6, 0, partner_ids)],
        # })

        # 指定主题为审批消息
        channel_entity.message_post(info, message_type='comment', subtype='mail.mt_comment')


    def process_buniess_logic(self):
        # ---> 投前
        # 投资决策申请 表名
        investment_decision_application = 'cowin_project.sub_invest_decision_app'

        # 投资决策委员会会议决议 表名
        investment_decision_res = 'cowin_project.sub_invest_decision_committee_res'

        # 投资决策委员会会议纪要 表名
        investment_decision_sum = 'cowin_project.sub_sum_invest_decision_committee'

        # ---> 投后
        # 投资退出申请书 表名
        investment_post_application = 'cowin_project.sub_app_invest_withdrawal'

        # 项目退出会议纪要 表名
        investment_post_sum = 'cowin_project.sub_sum_pro_withdraw_from_meeting'

        # 项目退出决议 表名
        investment_post_decision_res = 'cowin_project.sub_project_exit_resolution'

        if self.sub_project_tache_id.tache_id.model_id.model_name == investment_decision_res:
            # 投资决策委员会决议 需要开启 投资决策申请中子环节中的新增按钮
            res_entities = self.sub_project_tache_id.meta_sub_project_id.sub_tache_ids.filtered(
                lambda t: t.tache_id.model_id.model_name == investment_decision_application)

            # 拿到第一个 投资退出申请书 实体, 开启其新增操作
            res_entity = res_entities[0]

            # last_entity = self.sub_project_tache_id.meta_sub_project_id.sub_tache_ids.filtered(
            #     lambda e: e.tache_id.model_id.model_name == investment_decision_res and e.res_id == self.sub_project_tache_id.res_id)


            last_entity = self.env[investment_decision_res].browse(self.sub_project_tache_id.res_id)
            # 投资决策委员会会议决议  是否为为最终决议
            if last_entity.is_final_meeting_resolution:

                tmp = False
            else:
                tmp = True

            res_entity.write({
                'once_or_more': tmp
            })



        elif self.sub_project_tache_id.tache_id.model_id.model_name == investment_post_decision_res:
            # 项目退出决议 需要开启 投资退出申请书中子环节中的新增按钮
            res_entities = self.sub_project_tache_id.meta_sub_project_id.sub_tache_ids.filtered(
                lambda t: t.tache_id.model_id.model_name == investment_post_application)

            # 拿到第一个 投资退出申请书 实体, 开启其新增操作
            res_entity = res_entities[0]

            res_entity.write({
                'once_or_more': True
            })


        # 投资决策委员会会议纪要 所关联的投票表
        elif self.sub_project_tache_id.tache_id.model_id.model_name == investment_decision_sum:
            self.sub_project_tache_id.write_special_vote(True)

            # 项目退出会议纪要 有关联的表
        elif self.sub_project_tache_id.tache_id.model_id.model_name == investment_post_sum:
            self.sub_project_tache_id.write_special_vote(False)
        else:
            # 这种条件下,需要先依赖主环节重的 once_or_more
            if self.sub_project_tache_id.tache_id.once_or_more:
                tache_entities = self.meta_sub_project_id.sub_tache_ids & self.sub_project_tache_id.tache_id.tache_status_ids

                head_tache_entity = tache_entities[0]

                head_tache_entity.write({
                    'once_or_more': True,
                })
            self.sub_project_tache_id.trigger_next_subtache()


    # 改变状态的操作!!!
    def process_action(self):
        prevstatus, newstatus = self.prev_status, self.status
        sub_project_name = self.meta_sub_project_id.sub_project_ids[0].name
        round_financing_name = self.meta_sub_project_id.round_financing_and_Foundation_ids[0].round_financing_id.name
        foundation_name = self.meta_sub_project_id.round_financing_and_Foundation_ids[0].foundation_id.name

        sub_project_name = sub_project_name if sub_project_name else u''
        round_financing_name = round_financing_name if round_financing_name else u'暂无轮次'
        foundation_name = foundation_name if foundation_name else u'暂无基金'
        approval_role_name = self.current_approval_flow_node_id.operation_role_id.name


        approval_roel_person = self.env.user.employee_ids[0].name

        tmp2 = {}
        tmp2[u'sub_project_name'] = sub_project_name
        tmp2[u'round_financing_name'] = round_financing_name
        tmp2[u'foundation_name'] = foundation_name
        tmp2[u'approval_role_name'] = approval_role_name
        tmp2[u'approval_roel_person'] = approval_roel_person
        tmp2[u'operation_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 8 * 3600))
        tmp2[u'operation'] = u''
        tmp2[u'sub_tache_name'] = self.sub_project_tache_id.name


        if (prevstatus, newstatus) == (1, 2):
            print(u'(1, 2) aciton...')
            tmp2[u'operation'] = u'提交'
            self.message_post(json.dumps(tmp2))
            self.send_next_approval_flow_settings_node_msg(status=2)
            self.prev_status = self.status = newstatus
        elif (prevstatus, newstatus) == (1, 4):
            print(u'(1, 4) aciton...')
            tmp2[u'operation'] = u'提交'
            self.message_post(json.dumps(tmp2))
            self.prev_status = self.status = newstatus
            self.send_next_approval_flow_settings_node_msg(status=4)

            self.process_buniess_logic()


        elif (prevstatus, newstatus) == (2, 2):
            print(u'(2, 2) acion...')
            tmp2[u'operation'] = u'同意'
            self.message_post(json.dumps(tmp2))
            self.send_next_approval_flow_settings_node_msg(status=2)
            self.prev_status = self.status = newstatus
        elif (prevstatus, newstatus) == (2, 3):
            self.sub_project_tache_id.write({
                'is_launch_again': True,
            })
            tmp2[u'operation'] = u'暂缓'
            self.message_post(json.dumps(tmp2))
            self.send_next_approval_flow_settings_node_msg(status=3)
            self.prev_status = self.status = 1
        elif (prevstatus, newstatus) == (2, 4):
            tmp2[u'operation'] = u'同意'
            self.prev_status = self.status = newstatus
            self.message_post(json.dumps(tmp2))
            self.send_next_approval_flow_settings_node_msg(status=4)

            self.process_buniess_logic()

        elif (prevstatus, newstatus) == (2, 5):
            self.prev_status = self.status = newstatus
            tmp2[u'operation'] = u'拒绝'
            self.message_post(json.dumps(tmp2))
            self.send_next_approval_flow_settings_node_msg(status=5)

        elif (prevstatus, newstatus) == (6, 7):
            # 投票同意
            self.prev_status = self.status = newstatus
            tmp2[u'operation'] = u'投票同意'
            self.message_post(json.dumps(tmp2))
            self.send_next_approval_flow_settings_node_msg(status=7)
            self.sub_project_tache_id.trigger_next_subtache()

        elif (prevstatus, newstatus) == (6, 5):
            # 投票同意
            self.prev_status = self.status = newstatus
            tmp2[u'operation'] = u'投票拒绝'
            self.message_post(json.dumps(tmp2))
            self.send_next_approval_flow_settings_node_msg(status=3)

        else:
            pass







    def upate_status(self, new_status):

        '''
        :param new_status: 2(同意) 3 (暂缓) 5 (拒绝)
        :return:
        '''
        if new_status == 2:
            # if self.status != 2:
            #     raise UserWarning(u'未知的错误,审核环节不可能出现这类错误!!!')
            self.status = 2
            self.current_approval_flow_node_id = self.current_approval_flow_node_id.parent_id
            # self.process_action()
            if not self.current_approval_flow_node_id.parent_id:
                self.status = 4

        elif new_status == 3:
            # 暂缓
            self.status = 3
            self.current_approval_flow_node_id = self.approval_flow_settings_id.approval_flow_setting_node_ids[1]

        elif new_status == 5:
            self.status = 5

        elif new_status == 6:
            self.status = 6

        elif new_status == 7:
            self.status = 7

        else:
            pass

        self.process_action()




    def is_finish(self):

        if self.get_approval_flow_settings_nodes() == 2:
            self.current_approval_flow_node_id = self.current_approval_flow_node_id.parent_id
            self.prev_status = self.status = 4
            return True

        if self.is_success():
            return True

        return False

    def is_success(self):
        return self.status == 4

    def set_reject(self):
        if self.is_reject():
            return
        self.upate_status(5)

    def is_reject(self):

        return self.status == 5


    def get_all_sub_aproval_flow_settings_records(self):

        res = []
        for entity in self.sub_pro_approval_flow_settings_record_ids:
            res.append(entity.get_info())




        return {'current_approval_flow_node_id': self.current_approval_flow_node_id.id,
                'all_sub_aproval_flow_settings_records': res}

    # 当前审批节点的个数
    def get_approval_flow_settings_nodes(self):
        return len(self.approval_flow_settings_id.approval_flow_setting_node_ids)

    def is_approval_flow_status(self):
        return self.status == 2

    def is_final_approval_flow_settings_status(self):
        return self.status == 4 or self.status == 5

    # 能更新就更新
    # def update_final_approval_flow_settings_status_and_node(self):
    #     if self.is_final_approval_flow_settings_status():
    #         return True
    #
    #     # 当前审批节点的个数
    #     if self.get_approval_flow_settings_nodes() == 2:
    #         # prev = self.current_approval_flow_node_id
    #
    #         self.current_approval_flow_node_id = self.current_approval_flow_node_id.parent_id
    #
    #         if not self.current_approval_flow_node_id.parent_id:
    #             # self.current_approval_flow_node_id = prev
    #
    #             self.write({
    #                 'status': 4,
    #                 'current_approval_flow_node_id': self.current_approval_flow_node_id.id,
    #                 })
    #
    #             if (self.status, self.prev_status) == (1, 4):
    #                 # acton ...
    #                 print u'发起操作'
    #
    #             self.prev_status = self.status
    #
    #
    #             return True
    #
    #     return False

    #
    # def update_approval_flow_settings_status_and_node(self):
    #     if self.is_final_approval_flow_settings_status():
    #         return
    #
    #     # prev = self.current_approval_flow_node_id
    #     self.current_approval_flow_node_id = self.current_approval_flow_node_id.parent_id
    #
    #
    #
    #     # 如果到达审批结束节点,那么直接进入同意状态
    #     if not self.current_approval_flow_node_id.parent_id:
    #         # self.current_approval_flow_node_id = prev
    #         # self.status = 4
    #         self.write({
    #                 'status': 4,
    #                 # 'current_approval_flow_node_id': self.current_approval_flow_node_id.id,
    #                 'current_approval_flow_node_id': self.current_approval_flow_node_id.id,
    #             })
    #
    #         if (self.prev_status, self.status) == (2, 4):
    #             # action
    #             print(u'审核同意操作!!!')
    #
    #         self.prev_status = self.prev_status
    #
    #         # 需要触发下一个子环节
    #         self.sub_project_tache_id.check_or_not_next_sub_tache()
    #
    #
    #         return
    #
    #
    #     # 否则,目前讨论审核中的状态
    #     self.write({
    #         'status': 2,
    #         'current_approval_flow_node_id': self.current_approval_flow_node_id.id,
    #         })
    #
    #     if (self.prev_status, self.status) == (2, 2):
    #         # action
    #         print(u'继续审核操作!!!')





    def save_approval_flow_info(self, approval_flow_settings_record_info):
        status = approval_flow_settings_record_info['approval_result']
        # current_approval_flow_node_id = approval_flow_settings_record_info['current_approval_flow_node_id']


        # 这种情况下代表着出现多次并行的操作的问题!!!

        if self.is_final_approval_flow_settings_status():
            raise UserWarning(u'该审批已经被审核!!!')


        if status == True:      # 同意
            status = 2
            approval_flow_settings_record_info['approval_result'] = u'同意'
        elif status == False:   # 拒绝
            status = 5
            approval_flow_settings_record_info['approval_result'] = u'拒绝'
        elif status is None:    # 暂缓
            status = 3
            approval_flow_settings_record_info['approval_result'] = u'暂缓'
        else:
            pass

        self.upate_status(status)

        self.write({
            'sub_pro_approval_flow_settings_record_ids': [(0, 0, approval_flow_settings_record_info)]
        })

            # 根据审批得到的结果来获得是否是审批审批通过与否
        # if status == True:
        #     # 是否还处于审批状态
        #     if self.is_approval_flow_status():
        #         # 代表审批结束
        #         # self.status = 4
        #         self.update_approval_flow_settings_status_and_node()
        #
        #     approval_flow_settings_record_info['approval_result'] = u'同意'
        # if status == False:
        #     # 拒绝
        #     self.status = 5
        #
        #     if (self.status, self.prev_status) == (2, 5):
        #         # action
        #         print(u'暂缓action拒绝!!!')
        #         self.prev_status = self.status
        #
        #     approval_flow_settings_record_info['approval_result'] = u'拒绝'
        # if status is None:
        #     # 暂缓
        #     self.status = 3
        #
        #     if (self.status, self.prev_status) == (2, 3):
        #         # action
        #         print(u'暂缓action转移!!!')
        #         self.prev_status = self.status
        #
        #     # self.approval_flow_settings_id.approval_flow_setting_node_ids[1] 代表发起人
        #     # self.approval_flow_settings_id.approval_flow_setting_node_ids[0] 代表审批结束
        #     self.current_approval_flow_node_id = self.approval_flow_settings_id.approval_flow_setting_node_ids[1]
        #     self.sub_project_tache_id.write({
        #         'is_launch_again': True,
        #     })
        #
        #     approval_flow_settings_record_info['approval_result'] = u'暂缓'
        #
        # # approval_flow_settings_record_info['approval_result'] = u'同意' if approval_flow_settings_record_info[
        # #     'approval_result'] else u'不同意'
        #
        #
        #
        # self.write({
        #     'sub_pro_approval_flow_settings_record_ids': [(0, 0, approval_flow_settings_record_info)]
        # })

