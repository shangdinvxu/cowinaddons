# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Cowin_sub_project_approval_flow_settings(models.Model):
    _name = 'cowin_project.sub_approval_flow_settings'

    '''
        每个子工程都会有自己的审批流的,所以需要保存属于自己的审批流程的节点的信息
    '''


    name = fields.Char(string=u'子工程审批流节点信息')

    # tache_id = fields.Many2one('cowin_project.process_tache', string=u'环节')
    approval_flow_settings_id = fields.Many2one('cowin_project.approval_flow_settings', string=u'工程审批流', ondelete="restrict")
    meta_sub_project_id = fields.Many2one('cowin_project.meat_sub_project', string=u'元子工程实例', ondelete="cascade")

    status = fields.Selection([(1, u'发起'), (2, u'审核中'), (3, u'暂缓(从新发起)'), (4, u'同意'), (5, u'拒绝')],
                     string=u'审核状态', default=1)

    # is_putoff = fields.Boolean(string=u'是否暂缓', default=True)


    # status_trigger = fields.Integer(compute='_compute_status')


    # 用以记录当前的审批节点的位置

    current_approval_flow_node_id = fields.Many2one('cowin_project.approval_flow_setting_node',
                                                                    string=u'当前的审批节点所在的位置!!!')



    sub_pro_approval_flow_settings_record_ids = fields.One2many('cowin_project.sub_approval_flow_settings_record',
                                                                'sub_approval_settings_id', string=u'审批记录')

    # 构建子环节和子审批实体一对一的关系
    sub_project_tache_id = fields.Many2one('cowin_project.subproject_process_tache', string=u'子环节实体')



    def is_success(self):
        return self.status == 4

    def is_reject(self):

        return self.status == 3


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
    def update_final_approval_flow_settings_status_and_node(self):
        if self.is_final_approval_flow_settings_status():
            return True

        # 当前审批节点的个数
        if self.get_approval_flow_settings_nodes() == 2:
            # prev = self.current_approval_flow_node_id

            self.current_approval_flow_node_id = self.current_approval_flow_node_id.parent_id

            if not self.current_approval_flow_node_id.parent_id:
                # self.current_approval_flow_node_id = prev

                self.write({
                    'status': 4,
                    'current_approval_flow_node_id': self.current_approval_flow_node_id.id,
                    })


                return True

        return False


    def update_approval_flow_settings_status_and_node(self):
        if self.is_final_approval_flow_settings_status():
            return

        # prev = self.current_approval_flow_node_id
        self.current_approval_flow_node_id = self.current_approval_flow_node_id.parent_id



        # 如果到达审批结束节点,那么直接进入同意状态
        if not self.current_approval_flow_node_id.parent_id:
            # self.current_approval_flow_node_id = prev
            # self.status = 4
            self.write({
                    'status': 4,
                    # 'current_approval_flow_node_id': self.current_approval_flow_node_id.id,
                    'current_approval_flow_node_id': self.current_approval_flow_node_id.id,
                })

            # 需要触发下一个子环节
            self.sub_project_tache_id.check_or_not_next_sub_tache()


            return


        # 否则,目前讨论审核中的状态
        self.write({
            'status': 2,
            'current_approval_flow_node_id': self.current_approval_flow_node_id.id,
            })






    def save_approval_flow_info(self, approval_flow_settings_record_info):
        status = approval_flow_settings_record_info['approval_result']
        # current_approval_flow_node_id = approval_flow_settings_record_info['current_approval_flow_node_id']


        # 这种情况下代表着出现多次并行的操作的问题!!!

        if self.is_final_approval_flow_settings_status():
            raise UserWarning(u'该审批已经被审核!!!')


        # 根据审批得到的结果来获得是否是审批审批通过与否
        if status == True:
            # 是否还处于审批状态
            if self.is_approval_flow_status():
                # 代表审批结束
                # self.status = 4
                self.update_approval_flow_settings_status_and_node()

            approval_flow_settings_record_info['approval_result'] = u'同意'
        if status == False:
            # 拒绝
            self.status = 5

            approval_flow_settings_record_info['approval_result'] = u'拒绝'
        if status is None:
            # 暂缓
            self.status = 1
            # self.approval_flow_settings_id.approval_flow_setting_node_ids[1] 代表发起人
            # self.approval_flow_settings_id.approval_flow_setting_node_ids[0] 代表审批结束
            self.current_approval_flow_node_id = self.approval_flow_settings_id.approval_flow_setting_node_ids[1]
            self.sub_project_tache_id.write({
                'is_launch_again': True,
            })

            approval_flow_settings_record_info['approval_result'] = u'暂缓'

        # approval_flow_settings_record_info['approval_result'] = u'同意' if approval_flow_settings_record_info[
        #     'approval_result'] else u'不同意'



        self.write({
            'sub_pro_approval_flow_settings_record_ids': [(0, 0, approval_flow_settings_record_info)]
        })

