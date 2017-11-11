# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class Cowin_settings_process_tache(models.Model):
    _name = 'cowin_settings.process_tache'

    name = fields.Char(string=u'环节')
    parent_id = fields.Many2one('cowin_settings.process_tache', string=u'解锁条件')

    description = fields.Char(string=u'说明')
    state = fields.Boolean(string=u'启用状态', default=True)

    stage_id = fields.Many2one('cowin_settings.process_stage', ondelete="cascade")

    once_or_more = fields.Boolean(string=u'发起次数', default=False)

    model_id = fields.Many2one(u'cowin_settings.custome_model_data', string=u'自定义model的名字')

    res_id = fields.Integer(string=u'该环节对应该实例另一个字段model_id中的一个实例')

    # approval_flow_settings = fields.One2many('cowin_settings.approval_flow_settings', 'tache_id', string=u'审批流程')

    _sql_constraints = [
        ('login_key', 'UNIQUE (name)', u'环节配置名不能相同!!!')
    ]


    @api.model
    def create(self, vals):
        # entity = self.env['cowin_settings.custome_model_data'].search([('model_name', '=', 'cowin_project.cowin_project')])
        # if not entity:
        #     entity = entity.create({
        #         'name': 'cowin_project.cowin_project',
        #         'model_name': 'cowin_project.cowin_project'
        #     })

        res = super(Cowin_settings_process_tache, self).create(vals)
        # begin 添加审批流
        # res.write({'approval_flow_settings': res.get_approval_flow_settings()})

        # --end


        # res.model_name = entity
        return res


    def _check_parent_id(self, ids=[]):

        # 如果parent_id为空的情况下,到达了顶层
        if not self.parent_id.id:
            return True

        # 如果parent_id不为空的, 相互引用的话,直接返回为False
        # 不过,这里情况可以包含在抽象递归调用之中
        # if self.id == self.parent_id.id:
        #     return False

        # 如果便利的节点的列表为空的情况下,直接返回True
        # if not ids:
        #     return True

        if self.id in ids:
            return False

        ids.append(self.id)

        return self.parent_id._check_parent_id(ids)



    # 检查依赖的记录之间时候会有环的形成!!1
    def on_set_parent_id(self):
        ids = []
        print u'kkkk'
        return self._check_parent_id(ids)



    def get_approval_flow_settings(self):
        res = None
        if not self.approval_flow_settings:
            res = self.env['cowin_settings.approval_flow_settings'].create({'name': u'审批流'})
            res.tache_id = self

        else:
            res = self.approval_flow_settings
        return res