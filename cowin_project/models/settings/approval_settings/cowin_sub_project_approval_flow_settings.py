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


    # status_trigger = fields.Integer(compute='_compute_status')


    # 用以记录当前的审批节点的位置

    current_approval_flow_node_id = fields.Many2one('cowin_project.approval_flow_setting_node',
                                                                    string=u'当前的审批节点所在的位置!!!')



    sub_pro_approval_flow_settings_record_ids = fields.One2many('cowin_project.sub_approval_flow_settings_record',
                                                                'sub_approval_settings_id', string=u'审批记录')

    # 构建子环节和子审批实体一对一的关系
    sub_project_tache_id = fields.Many2one('cowin_project.subproject_process_tache', string=u'子环节实体')

    # def status_trigger_m(self):
    #     self.status_trigger
    #
    # @api.depends('status')
    # def _compute_status(self):
    #     # self.ensure_one()
    #     for record in self:
    #         record.status_trigger = record.status
    #         print(u'数据库的问题吗?')
    #
    #         if record.status == 4:
    #             # 触发下一个子环节操作
    #             for sub_tache_entity in record.meta_sub_project_id.sub_tache_ids:
    #                 if sub_tache_entity.parent_id == record.sub_project_tache_id:
    #                     sub_tache_entity.write({
    #                         'is_unlocked': True,
    #                         })
    #                     break
    #
    #
    #         elif self.status == 3:
    #             # 暂缓
    #             pass
    #
    #         elif self.status == 5:
    #             # 拒绝
    #             pass
    #
    #     i = 0


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


    def get_approval_flow_settings_nodes(self):
        return len(self.approval_flow_settings_id.approval_flow_setting_node_ids)

    def update_final_approval_flow_settings_status_and_node(self):
        if self.status == 4:
            return True

        if self.get_approval_flow_settings_nodes() == 2:

            self.current_approval_flow_node_id = self.current_approval_flow_node_id.parent_id

            self.write({
                'status': 4,
                'current_approval_flow_node_id': self.current_approval_flow_node_id.id,
                })

            return True

        return False


    def update_approval_flow_settings_status_and_node(self):
        if self.status == 4 or self.status == 5:
            return

        self.current_approval_flow_node_id = self.current_approval_flow_node_id.parent_id

        # 如果没有审核人,那么直接进入同意状态
        if not self.current_approval_flow_node_id.parent_id:
            # self.status = 4
            self.write({
                    'status': 4,
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

        if self.status == 4 or self.status == 5:
            raise UserWarning(u'该审批已经被审核!!!')

        # 状态设定的更改,位置的顺序很重要,和下一句!!!
        # self.status = 4 if approval_flow_settings_record_info['approval_result'] else 5

        # 根据审批得到的结果来获得是否是审批审批通过与否
        if status == True:
            # 同意
            # self.current_approval_flow_node_id = True
            self.current_approval_flow_node_id = self.current_approval_flow_node_id.parent_id
            if not self.current_approval_flow_node_id.parent_id:
                # 代表审批结束
                # self.status = 4
                self.update_approval_flow_settings_status_and_node()
                # self.write({
                #     'status': 4,
                #     })
            approval_flow_settings_record_info['approval_result'] = u'同意'
        if status == False:
            # 拒绝
            # self.status = 5
            self.write({
                'status': 5,
                })
            approval_flow_settings_record_info['approval_result'] = u'拒绝'
        if status is None:
            # 暂缓
            # self.status = 3
            self.write({
                'status': 3,
                })
            approval_flow_settings_record_info['approval_result'] = u'暂缓'

        # approval_flow_settings_record_info['approval_result'] = u'同意' if approval_flow_settings_record_info[
        #     'approval_result'] else u'不同意'



        self.write({
            'sub_pro_approval_flow_settings_record_ids': [(0, 0, approval_flow_settings_record_info)]
        })

