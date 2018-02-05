# -*- coding: utf-8 -*-
from odoo import models, fields, api
import json
from odoo.tools.mail import html_sanitize, html2plaintext
import time

from odoo.exceptions import UserError

from odoo import SUPERUSER_ID
class Cowin_sub_project_approval_flow_settings(models.Model):
    # _inherit = ['mail.thread']

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

    approval_flow_count = fields.Integer(string=u'审核次数', default=0, help=u'用以甄别当前审核的可能发生重新发起等操作,也是用来' +
                                                                         u'解决多个用户同时审核的问题!!!')


    is_launch_again = fields.Boolean(string=u'是否是重新提交的状态', default=False)


    def get_all_message(self):
        message_entities = self.env['mail.message'].search([('subject', '=', 'approval_flow_setting'), ('res_id', '=', self.id), ('model', '=', self._name)])
        message_infos = message_entities.mapped(lambda m: html2plaintext(m.body))

        return message_infos


    def send_current_approval_flow_settings_node_msg(self, status):
        self.send_approval_flow_settings_node_msg(status, True)


    def send_next_approval_flow_settings_node_msg(self, status):
        self.send_approval_flow_settings_node_msg(status, False)


    def send_approval_flow_settings_node_msg(self, status=2, is_current_or_next=True):
        sub_project_name = self.meta_sub_project_id.sub_project_ids[0].name
        round_financing_name = self.meta_sub_project_id.round_financing_and_Foundation_ids[0].round_financing_id.name
        foundation_name = self.meta_sub_project_id.round_financing_and_Foundation_ids[0].foundation_id.name

        sub_project_name = sub_project_name if sub_project_name else u''
        round_financing_name = round_financing_name if round_financing_name else u'暂无轮次'
        foundation_name = foundation_name if foundation_name else u'暂无基金'

        tes = prev = self.current_approval_flow_node_id

        if not is_current_or_next:
            tes = next = self.current_approval_flow_node_id.parent_id

        # approval_role_name = self.current_approval_flow_node_id.operation_role_id.name
        approval_role_name = tes.operation_role_id.name


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

        if status == 1:   # 提交的操作
            if self.is_launch_again:
                tmp2[u'operation'] = u'重新提交'
                info = info_first + u'您重新提交了[%s]' % self.sub_project_tache_id.name
            else:
                tmp2[u'operation'] = u'提交'

                info = info_first + u'您提交了[%s]' % self.sub_project_tache_id.name

        elif status == 2: # 待审批


            tmp2[u'operation'] = u'待处理'

            info = info_first + u'您有一项[%s] 待处理' % self.sub_project_tache_id.name

        elif status == 3:
            info = info_first + u'您发起的[%s] 已暂缓' % self.sub_project_tache_id.name
        elif status == 4:
            info = info_first + u'您发起的[%s] 已审批通过' % self.sub_project_tache_id.name
        elif status == 5:
            info = info_first + u'您发起的[%s] 已拒绝' % self.sub_project_tache_id.name

        elif status == 6:
            tmp2[u'operation'] = u'投票'
            info = info_first + u'您收到一条[%s]提醒' % self.sub_project_tache_id.name


        elif status == 7:
            info = info_first + u'您的[%s] 已投票通过' % self.sub_project_tache_id.name

        else:
            tmp2[u'operation'] = u''






        if status == 6:  # 投票的消息
            partner_ids = self.meta_sub_project_id.investment_decision_committee_scope_id.employee_ids.mapped(
                'user_id.partner_id.id')
            channel_entity = self.env.ref('cowin_project.init_project_mail_channel')
            channel_entity.write({
                'channel_partner_ids': [(6, 0, partner_ids)],
            })
            channel_entity.message_post(info, message_type='comment', subtype='mail.mt_comment')
        else:  # 普通消息

            def send_message_():
                if is_current_or_next:  # 当前发送消息
                    channel_entity = self.env.ref('cowin_project.init_project_mail_channel')

                    channel_entity.write({
                        'channel_partner_ids': [(6, 0, [self.env.user.partner_id.id])],
                    })
                    # 指定主题为审批消息
                    channel_entity.message_post(info, message_type='comment', subtype='mail.mt_comment')
                else:
                    approval_role = tes.operation_role_id
                    channel_entity = self.env.ref('cowin_project.init_project_mail_channel')
                    # 当前的用户
                    rel_entities = self.meta_sub_project_id.sub_meta_pro_approval_settings_role_rel & approval_role.sub_meta_pro_approval_settings_role_rel

                    partner_ids = list(map(lambda rel: rel.employee_id.user_id.partner_id.id, rel_entities))
                    id = self.env['res.users'].search([('id', '=', 1)]).partner_id.id
                    partner_ids.append(id)

                    channel_entity.write({
                        'channel_partner_ids': [(6, 0, [self.env.user.partner_id.id])],
                    })
                    channel_entity.message_post(info, message_type='comment', subtype='mail.mt_comment')

            send_message_()


        self.current_approval_flow_node_id = prev






    # 处理关于审核中暂缓状态的操作!!!
    def process_put_off_staus(self):
        # model_name = self.sub_project_tache_id.tache_id.model_id.model_name
        # res_id = self.sub_project_tache_id.res_id
        #
        # target_entity = self.env[model_name].browse(res_id)
        #
        # target_entity.write({
        #     'inner_or_outer_status': 3,
        # })

        self.sub_project_tache_id.write({
            'is_launch_again': True,
        })

        self.status = self.prev_status = 1



    # 暂缓状态中,关于button按钮状态变化的系列
    def process_button_status_on_res_model(self, status):

        model_name = self.sub_project_tache_id.tache_id.model_id.model_name
        res_id = self.sub_project_tache_id.res_id

        target_entity = self.env[model_name].browse(res_id)

        if status == 3:
            # 暂缓
            t = 0
        elif status == 4:
            # 同意
            t = 2
        elif status == 5:
            # 拒绝
            t = 2
        else:
            t = 2

        target_entity.write({
            'button_status': t,
        })


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

        # 尽调报告  表名
        subt_dispatch_report = 'cowin_project.subt_dispatch_report'



        # 项目立项 表名

        cowin_project_cowin_subproject_name = 'cowin_project.cowin_subproject'

        if self.sub_project_tache_id.tache_id.model_id.model_name == investment_decision_res:
            # 投资决策委员会决议 需要开启 投资决策申请中子环节中的新增按钮

            res_entities = self.sub_project_tache_id.meta_sub_project_id.sub_tache_ids.filtered(
                lambda t: t.tache_id.model_id.model_name == investment_decision_application)

            # 拿到第一个 投资退出申请书 实体, 开启其新增操作
            res_entity = res_entities[0]


            last_entity = self.env[investment_decision_res].browse(self.sub_project_tache_id.res_id)
            # 投资决策委员会会议决议  是否为为最终决议
            if last_entity.is_final_meeting_resolution:
                # 在为是最终决议的条件下,需要开启主工程 新增基金轮次实体接口
                self.process_new_round_fund_entity()

                # 需要把 投资决策申请子环节的新增按钮禁用!!!  默认我们去第一条即可
                res_entity.write({
                    'once_or_more': False,
                })

                # 触发下一个子环节!!!
                self.sub_project_tache_id.trigger_next_subtache()

                # 投委会决议票审核通过之后, 将该基金投资信息存入项目详情内, (该操作与项目主流程无关)
                if self.sub_project_tache_id.meta_sub_project_id.round_financing_and_Foundation_ids:
                    entity = self.sub_project_tache_id.meta_sub_project_id.round_financing_and_Foundation_ids[0]
                    round_env = self.env['cowin.project.detail.round']
                    round_ = round_env.search([
                        ('project_id', '=', self.meta_sub_project_id.project_id.id),
                        ('round_financing_id', '=', entity.foundation_id.id),
                    ])
                    if round_:
                        self.env['cowin.project.detail.foundation'].create({
                            'round_id': round_.id,
                            'ownership_interest': entity.ownership_interest,
                            'meta_sub_project_id': self.meta_sub_project_id.id,
                            'the_amount_of_investment': entity.the_amount_of_financing,
                            'foundation': entity.foundation_id.name,
                            'data_from': 'local'
                        })
                    else:
                        round_env.create({
                            'project_id': self.meta_sub_project_id.project_id.id,
                            'round_financing_id': entity.foundation_id.id,
                            'the_amount_of_financing': entity.the_amount_of_investment,
                            'project_valuation': entity.project_valuation,
                            'foundation_ids': [(0, 0, {
                                'ownership_interest': entity.ownership_interest,
                                'meta_sub_project_id': self.meta_sub_project_id.id,
                                'the_amount_of_investment': entity.the_amount_of_financing,
                                'foundation': entity.foundation_id.name,
                                'data_from': 'local'
                            })]
                        })
            else:
                res_entity.write({
                    'once_or_more': True,
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

            # 触发下一个子环节!!!
            self.sub_project_tache_id.trigger_next_subtache()

            # 退出时将信息存入项目详情-退出信息中, 此操作与主流程无关
            if self.sub_project_tache_id.meta_sub_project_id.round_financing_and_Foundation_ids:

                exit_entity = self.env[investment_post_decision_res].browse(self.sub_project_tache_id.res_id)
                entity = self.sub_project_tache_id.meta_sub_project_id.round_financing_and_Foundation_ids[0]
                project_id = self.sub_project_tache_id.meta_sub_project_id.project_id.id

                round_id = self.env['cowin.project.detail.round'].sudo().search([
                    ('project_id', '=', project_id),
                    ('round_financing_id', '=', entity.foundation_id.id),
                ])

                foundation_id = self.env['cowin.project.detail.foundation'].sodu().search([
                    ('round_id', '=', round_id.id),
                    ('foundation', '=', entity.foundation_id.name),
                    ('data_from', '=', 'local'),
                ])
                if foundation_id:
                    self.env['cowin.project.detail.withdrawals'].create({
                        'foundation_id': foundation_id.id,
                        'the_amount_of_withdrawals': exit_entity.withdrawal_amount,
                        'project_valuation': exit_entity.withdrawal_valuation,
                    })


        # 投资决策委员会会议纪要 所关联的投票表
        elif self.sub_project_tache_id.tache_id.model_id.model_name == investment_decision_sum:
            self.sub_project_tache_id.write_special_vote(True)

            # 项目退出会议纪要 有关联的表
        elif self.sub_project_tache_id.tache_id.model_id.model_name == investment_post_sum:
            self.sub_project_tache_id.write_special_vote(False)

        # 尽调报告 需要写入审核成功的日期   字段: 尽调审核日期
        elif self.sub_project_tache_id.tache_id.model_id.model_name == subt_dispatch_report:
            res_id = self.sub_project_tache_id.res_id
            res = self.env[subt_dispatch_report].browse(res_id)
            res.write({
                'date_of_review': fields.Date.today(),
            })

            # 把数据写入到指定的依赖的表中
            res.write_date_of_review_to_related_model()

            # 触发下一个子环节!!!
            self.sub_project_tache_id.trigger_next_subtache()

        elif self.sub_project_tache_id.tache_id.model_id.model_name == cowin_project_cowin_subproject_name:
            # 项目立项 所需要的数据
            res_id = self.sub_project_tache_id.res_id
            self.env[cowin_project_cowin_subproject_name].browse(res_id).write({
                'date_of_project': fields.Date.today(),
            })

            self.sub_project_tache_id.trigger_next_subtache()
        else:
            # 这种条件下,需要先依赖主环节中的 once_or_more
            if self.sub_project_tache_id.tache_id.once_or_more:
                tache_entities = self.meta_sub_project_id.sub_tache_ids & self.sub_project_tache_id.tache_id.tache_status_ids

                head_tache_entity = tache_entities[0]

                head_tache_entity.write({
                    'once_or_more': True,
                })
            self.sub_project_tache_id.trigger_next_subtache()

    # 设定所有的子环节 once_or_more 为Fasle
    def set_all_sub_tache_entities_once_or_more_to_false(self):
        for sub_e in self.meta_sub_project_id.sub_tache_ids:
            if sub_e.is_unlocked and not sub_e.view_or_launch:
                sub_e.write({
                    'is_unlocked': False,
                })
            elif sub_e.is_unlocked and sub_e.view_or_launch and sub_e.once_or_more:
                sub_e.write({
                    'once_or_more': False,
                })
            else:
                pass

    # 处理投资抉择委员会议决议表 为最终决议 或者是 拒绝的情况   即, 需要添加可以添加新的基金伦次实体
    def process_new_round_fund_entity(self):
        investment_decision_res = 'cowin_project.sub_invest_decision_committee_res'
        if self.sub_project_tache_id.tache_id.model_id.model_name == investment_decision_res:
            # 当前主工程新增的按钮变为可用状态
            self.meta_sub_project_id.project_id.write({
                'whether_new_meta_sub_project_or_not': True,
            })



    def process_approval_flow_count(self):

        self.approval_flow_count += 1


        # model_name = self.sub_project_tache_id.tache_id.model_id.model_name
        # res_id = self.sub_project_tache_id.res_id
        #
        # target_entity = self.env[model_name].browse(res_id)
        #
        # target_entity.write({
        #     'sub_approval_flow_settings_approval_flow_count': self.approval_flow_count,
        # })





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
            self.send_current_approval_flow_settings_node_msg(status=1)
            self.send_next_approval_flow_settings_node_msg(status=2)
            self.launch_or_relaunch_agin(self.is_launch_again)
            self.prev_status = self.status = newstatus
        elif (prevstatus, newstatus) == (1, 4):
            print(u'(1, 4) aciton...')
            tmp2[u'operation'] = u'提交'
            # self.message_post(json.dumps(tmp2))
            self.prev_status = self.status = newstatus
            self.send_current_approval_flow_settings_node_msg(status=1)
            self.send_next_approval_flow_settings_node_msg(status=4)
            # 增加校验操作
            self.process_button_status_on_res_model(status=4)


            self.process_buniess_logic()
            self.launch_or_relaunch_agin(self.is_launch_again)

        elif (prevstatus, newstatus) == (2, 2):
            print(u'(2, 2) acion...')
            tmp2[u'operation'] = u'同意'


            # self.message_post(json.dumps(tmp2))
            # self.send_current_approval_flow_settings_node_msg(status=2)
            self.send_next_approval_flow_settings_node_msg(status=2)
            self.prev_status = self.status = newstatus
        elif (prevstatus, newstatus) == (2, 3):
            tmp2[u'operation'] = u'暂缓'
            self.process_put_off_staus()

            # self.message_post(json.dumps(tmp2))
            # self.send_current_approval_flow_settings_node_msg(status=2)
            self.send_next_approval_flow_settings_node_msg(status=3)
            # self.prev_status = self.status = 1

            self.process_button_status_on_res_model(3)
            self.is_launch_again = True


        elif (prevstatus, newstatus) == (2, 4):
            tmp2[u'operation'] = u'同意'
            self.prev_status = self.status = newstatus
            # self.message_post(json.dumps(tmp2))
            # self.send_current_approval_flow_settings_node_msg(status=2)
            self.send_next_approval_flow_settings_node_msg(status=4)
            # 增加校验操作
            self.process_button_status_on_res_model(4)
            self.process_buniess_logic()


        elif (prevstatus, newstatus) == (2, 5):
            self.prev_status = self.status = newstatus
            tmp2[u'operation'] = u'拒绝'
            # self.message_post(json.dumps(tmp2))
            # self.send_current_approval_flow_settings_node_msg(status=2)
            self.send_next_approval_flow_settings_node_msg(status=5)

            # 设定所有的子环节 once_or_more 为False
            self.set_all_sub_tache_entities_once_or_more_to_false()

            # 处理投资抉择委员会议决议表 拒绝的情况   即, 需要添加可以添加新的基金伦次实体
            self.process_new_round_fund_entity()


            # 审批拒绝操作的时候,也是需要改变相应的模型的button的按钮的状态!!!
            self.process_button_status_on_res_model(5)

        elif (prevstatus, newstatus) == (6, 7):
            # 投票同意
            self.prev_status = self.status = newstatus
            tmp2[u'operation'] = u'投票同意'
            # self.message_post(json.dumps(tmp2))
            # self.send_current_approval_flow_settings_node_msg(status=6)
            self.send_next_approval_flow_settings_node_msg(status=7)
            self.sub_project_tache_id.trigger_next_subtache()

            self.process_button_status_on_res_model(4)

        elif (prevstatus, newstatus) == (6, 5):
            # 投票同意
            self.prev_status = self.status = newstatus
            tmp2[u'operation'] = u'投票拒绝'
            # self.message_post(json.dumps(tmp2))
            # self.send_current_approval_flow_settings_node_msg(status=6)
            self.send_next_approval_flow_settings_node_msg(status=3)

            # 设定所有的子环节 once_or_more 为Fasle
            self.set_all_sub_tache_entities_once_or_more_to_false()
            self.process_button_status_on_res_model(5)


        else:
            pass


        # 增加校验操作
        self.process_approval_flow_count()





    def upate_status(self, new_status):

        '''
        :param new_status: 2(同意) 3 (暂缓) 5 (拒绝)
        :return:
        '''
        if new_status == 2:
            # if self.status != 2:
            #     raise UserWarning(u'未知的错误,审核环节不可能出现这类错误!!!')
            self.status = 2
            # 该审核节点完成!!!
            self.current_approval_flow_node_id.write({
                'status': True,
            })
            self.current_approval_flow_node_id = self.current_approval_flow_node_id.parent_id


            if not self.current_approval_flow_node_id.parent_id:
                self.status = 4

        elif new_status == 3:
            # 暂缓
            self.status = 3
            # 暂缓之后,所有的审批节点重置
            self.approval_flow_settings_id.approval_flow_setting_node_ids.write({
                'status': False,
            })
            self.current_approval_flow_node_id = self.approval_flow_settings_id.approval_flow_setting_node_ids[1]

        elif new_status == 5:
            self.status = 5

        elif new_status == 6:
            self.status = 6
            self.send_next_approval_flow_settings_node_msg(status=6)

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


    # 发起/重新发起的需要记录的操作
    def launch_or_relaunch_agin(self, is_launch_agin=False):
        approval_flow_settings_record_info = {}
        approval_flow_settings_record_info['res_model'] = self.sub_project_tache_id.tache_id.model_id.model_name
        approval_flow_settings_record_info['res_id'] = self.sub_project_tache_id.res_id

        if is_launch_agin:
            approval_flow_settings_record_info['approval_result'] = u'重新发起'
        else:
            approval_flow_settings_record_info['approval_result'] = u'发起'

        # 理论上只会有一个员工  审批人
        approval_flow_settings_record_info['approval_person_id'] = self.env.user.employee_ids[0].id

        # 审批角色
        # approval_flow_settings_record_info['approval_role_id'] = self.current_approval_flow_node_id.operation_role_id.id
        approval_flow_settings_record_info['approval_role_id'] = self.approval_flow_settings_id.approval_flow_setting_node_ids[1].operation_role_id.id

        self.write({
            'sub_pro_approval_flow_settings_record_ids': [(0, 0, approval_flow_settings_record_info)]
        })

        self.approval_flow_count += 1




    def save_approval_flow_info(self, approval_flow_settings_record_info):
        status = approval_flow_settings_record_info['approval_result']
        # current_approval_flow_node_id = approval_flow_settings_record_info['current_approval_flow_node_id']

        # 这种情况下代表着出现多次并行的操作的问题!!!




        if self.is_final_approval_flow_settings_status():
            raise UserError(u'该审批早已审核完成!!!')

        approval_flow_settings_record_info['approval_flow_count'] = self.approval_flow_count

        # approval_flow_settings_record_info['res_model'] = self.sub_project_tache_id.tache_id.model_id.model_name
        # approval_flow_settings_record_info['res_id'] = self.sub_project_tache_id.res_id
        if status == u'True':      # 同意
            status = 2
            approval_flow_settings_record_info['approval_result'] = u'同意'
        elif status == u'False':   # 拒绝
            status = 5
            approval_flow_settings_record_info['approval_result'] = u'拒绝'
        elif status == u'None':    # 暂缓
            status = 3
            approval_flow_settings_record_info['approval_result'] = u'暂缓'
        else:
            pass

        # approval_flow_settings_record_info['approval_flow_count'] = self.approval_flow_count

        # 审批操作的数据



        self.write({
            'sub_pro_approval_flow_settings_record_ids': [(0, 0, approval_flow_settings_record_info)]
        })

        self.upate_status(status)








