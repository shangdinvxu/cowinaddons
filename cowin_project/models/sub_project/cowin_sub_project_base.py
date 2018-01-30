# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import MissingError, UserError


# 基类,需要派生操作!!!
class Cowin_sub_project_base_status(models.Model):
    _name = 'cowin_project.base_status'




    inner_or_outer_status = fields.Selection([(1, u'内部调用'), (2, u'外部调用'), (3, u'button调用')], string=u'子工程中,实体的状态', default=1)

    button_status = fields.Selection([(0, u'初始化'), (1, u'使用中') , (2, u'已完成')], string=u'button状态的改变', default=0)


    # 要和审批实体的数据的版本号匹配
    sub_approval_flow_settings_approval_flow_count = fields.Integer(string=u'数据版本号')






    def button_approval_flow_info(self, a, b, c):
        print(u'sub_approval_flow_settings_approval_flow_count is %s' % self._context.get('sub_approval_flow_settings_approval_flow_count'))

        # if self._context.get('sub_approval_flow_settings_approval_flow_count') != self.sub_approval_flow_settings_approval_flow_count:
        #    return self.env['cowin_common.common_dialog'].show_dialog()


        # return self.env['cowin_common.common_dialog'].show_dialog()

        if self.button_status == 2:
            raise UserError(u'已审核完毕')

        if self.button_status == 0:
            self.button_status = 1

        is_put_off = self.sub_tache_id.sub_pro_approval_flow_settings_ids.current_approval_flow_node_id.put_off
            # is_put_off = self.sub_tache_id.sub_pro_approval_flow_settings_ids.approval_flow_settings_id.put_off

        res = self.env['cowin_common.approval_flow_dialog'].create({
            'res_model': self._name,
            'res_id': self.id,
            'is_put_off': is_put_off,

        })


        # 获得审核过程中,该环节的名字
        tache_name = self.sub_tache_id.name

        return {
            'name': tache_name,
            'type': 'ir.actions.act_window',
            'res_model': res._name,
            'views': [[False, 'form']],
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_id': res.id,
            'target': 'new',
            # 用以说明当前的审批的数据版本号,  用以对数据的校检操作
            # 'context': {'sub_approval_flow_settings_approval_flow_count': self.sub_tache_id.sub_pro_approval_flow_settings_ids.approval_flow_count}
            'context': {'sub_approval_flow_settings_approval_flow_count': self.sub_approval_flow_settings_approval_flow_count}
        }


    # 查看审核结果
    def approval_view_action_action(self):
        name = self._name + '_form_no_button'
        view_id = self.env.ref(name).id

        return {
            'name': self._name,
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'views': [[view_id, 'form']],
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_id': self.id,
            'target': 'current',
        }



    # 审核界面的操作

    def approval_launch_action(self):
        name = self._name + '_form'
        view_id = self.env.ref(name).id
        # view_id = self.env.ref('cowin_project.sub_project_establishment_form').id

        return {
            'name': self._name,
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'views': [[view_id, 'form']],
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_id': self.id,
            'target': 'current',
        }






