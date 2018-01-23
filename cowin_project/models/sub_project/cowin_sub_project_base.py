# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import MissingError, UserError


# 基类,需要派生操作!!!
class Cowin_sub_project_base_status(models.Model):
    _name = 'cowin_project.base_status'




    inner_or_outer_status = fields.Selection([(1, u'内部调用'), (2, u'外部调用'), (3, u'button调用')], string=u'子工程中,实体的状态', default=1)

    button_status = fields.Selection([(0, u'初始化'), (1, u'使用中') , (2, u'已完成')], string=u'button状态的改变', default=0)







    def button_approval_flow_info(self, a, b, c):

        if self.button_status == 2:
            raise UserError(u'已审核完毕')

        if self.button_status == 0:
            self.button_status = 1


        res = self.env['cowin_common.approval_flow_dialog'].create({
            'res_model': self._name,
            'res_id': self.id,
        })

        return {
            'name': res._name,
            'type': 'ir.actions.act_window',
            'res_model': res._name,
            'views': [[False, 'form']],
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_id': res.id,
            'target': 'new',
        }













