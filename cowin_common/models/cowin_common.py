# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import MissingError, UserError

# 行业model
class Cowin_Common(models.Model):
    _name = 'cowin_common.cowin_industry'

    name = fields.Char(string=u'行业', required=True)

    _sql_constraints = [
        ('industry_key', 'UNIQUE (name)', u'行业名不能相同')
    ]


#项目来源
class Cowin_common_project_source(models.Model):
    _name = 'cowin_common.project_source'

    name = fields.Char(string=u'项目来源', required=True)

    _sql_constraints = [
            ('name_key', 'UNIQUE (name)', u'来源名不能够相同')
        ]


# 轮次model
class Cowin_round_financing(models.Model):
    _name = 'cowin_common.round_financing'

    name = fields.Char(string=u'轮次')

    _sql_constraints = [
            ('name_key', 'UNIQUE (name)', u'轮次名不能够相同')
        ]



# 审批角色
class Cowin_common_approval_role(models.Model):

    _name = 'cowin_common.approval_role'

    '''
        审批角色
    '''


    name = fields.Char(string=u'角色名')

    # user_ids = fields.Many2many('res.users', string=u'用户')

    _sql_constraints = [
        ('name_key', 'UNIQUE (name)', u'审批角色名称不能相同!!!'),
    ]




class Cowin_common_approval_flow_dialog(models.Model):
    _name = 'cowin_common.approval_flow_dialog'


    # name = fields.Char(string=u'审批人')


    res_model = fields.Char(string=u'审批的表名')
    res_id = fields.Integer(string=u'审批的实体')

    status = fields.Boolean(string=u'是否审批完成', default=False)

    approval_result = fields.Char(string=u'审批结果')
    approval_opinion = fields.Text(string=u'审批意见')


    def process_approval_flow_info(self):
        sub_tache_entity = self.env[self.res_model].browse(self.res_id).sub_tache_id

        # 子流程配置实体
        sub_approval_flow_settings_entity = sub_tache_entity.sub_pro_approval_flow_settings_ids

        approval_flow_settings_record_info = {
            # 理论上只会有一个员工  审批人
            'approval_person_id': self.env.user.employee_ids[0].id,
            # 审批角色
            'approval_role_id': sub_approval_flow_settings_entity.current_approval_flow_node_id.operation_role_id.id,

            'approval_result': self.approval_result,

            'res_model': self.res_model,
            'res_id': self.res_id,

        }
        # 更新审批节点 拿到当前的子环节
        sub_approval_flow_settings_entity.save_approval_flow_info(approval_flow_settings_record_info)







    @api.multi
    def button_agree(self):
        if self.status:
            raise UserError(u'已审批完成')
        self.status = True
        self.approval_result = u'True'
        self.process_approval_flow_info()




    @api.multi
    def button_reject(self):
        if self.status:
            raise UserError(u'已审批完成')
        self.status = True
        self.approval_result = u'False'
        self.process_approval_flow_info()

    @api.multi
    def button_putoff(self):
        if self.status:
            raise UserError(u'已审批完成')
        self.status = True
        self.approval_result = u'None'
        self.process_approval_flow_info()



