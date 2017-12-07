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

    status = fields.Selection([(1, u'暂无'), (2, u'审核中'), (3, u'暂缓'), (4, u'同意'), (5, u'拒绝')],
                     string=u'审核状态', default=1)


    # 用以记录当前的审批节点的位置

    current_approval_flow_node_id = fields.Many2one('cowin_project.approval_flow_setting_node',
                                                                    string=u'当前的审批节点所在的位置!!!')



    sub_pro_approval_flow_settings_record_ids = fields.One2many('cowin_project.sub_approval_flow_settings_record',
                                                                'sub_approval_settings_id', string=u'审批记录')




    # 构建子环节和子审批实体一对一的关系
    sub_project_tache_id = fields.Many2one('cowin_project.subproject_process_tache', string=u'子环节实体')


    def is_success(self):
        return self.status == 4


    def get_all_sub_aproval_flow_settings_records(self):

        res = []
        for entity in self.sub_pro_approval_flow_settings_record_ids:
            res.append(entity.get_info())


        return res



    def save_approval_flow_info(self, approval_flow_settings_record_info):

        # 状态设定的更改,位置的顺序很重要,和下一句!!!
        self.status = 4 if approval_flow_settings_record_info['approval_result'] else 5


        approval_flow_settings_record_info['approval_result'] = u'同意' if approval_flow_settings_record_info[
            'approval_result'] else u'不同意'

        self.write({
            'sub_pro_approval_flow_settings_record_ids': [(0, 0, approval_flow_settings_record_info)]
        })

