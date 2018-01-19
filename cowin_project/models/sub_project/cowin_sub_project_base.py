# -*- coding: utf-8 -*-
from odoo import models, fields, api


# 基类,需要派生操作!!!
class Cowin_sub_project_base_status(models.Model):
    _name = 'cowin_project.base_status'




    inner_or_outer_status = fields.Selection([(1, u'内部调用'), (2, u'外部调用')], string=u'子工程中,实体的状态', default=1)


    def return_approval_flow_again_form(self):


        return {
            'name': self._name,
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'views': [[False, 'form']],
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_id': self.id,
            'target': 'new',
            'flags': {'form': {'action_buttons': True, 'options': {'mode': 'edit'}}},

        }













