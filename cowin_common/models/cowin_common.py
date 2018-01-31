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

    sequence = fields.Integer(string=u'序列')

    _sql_constraints = [
            ('name_key', 'UNIQUE (name)', u'轮次名不能够相同'),
            ('sequence_key', 'UNIQUE (sequence)', u'轮次序列不能够相同')
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

    approval_flow_count = fields.Integer(string=u'用以和自审批实体做匹配,以便于审核过程中出现错误!!!')


    is_put_off = fields.Boolean(string=u'是否开启暂缓的标志!!!', default=True)

    def process_approval_flow_info(self):



        target_entity = self.env[self.res_model].browse(self.res_id)
        sub_tache_entity = target_entity.sub_tache_id

        # 子流程配置实体
        sub_approval_flow_settings_entity = sub_tache_entity.sub_pro_approval_flow_settings_ids

        res_1s = sub_approval_flow_settings_entity.current_approval_flow_node_id.operation_role_id.sub_meta_pro_approval_settings_role_rel

        res_2s = sub_approval_flow_settings_entity.meta_sub_project_id.sub_meta_pro_approval_settings_role_rel

        is_target_user = False

        for res_entity in res_2s & res_1s:
            if res_entity.employee_id.user_id == self.env.user:
                is_target_user = True

            break


        if not is_target_user:
            if self.env.user.id == 1:
                is_target_user = True


        # if not is_target_user:
        #     raise UserError(u'该用户不具有审批资格,或许已经进入到下一个审批')

        # if self._context.get('sub_approval_flow_settings_approval_flow_count') != target_entity.sub_approval_flow_settings_approval_flow_count:
        #     raise UserError(u'该用户不具有审批资格,或许已经进入到下一个审批')


        approval_flow_settings_record_info = {
            # 理论上只会有一个员工  审批人
            'approval_person_id': self.env.user.employee_ids[0].id,
            # 审批角色
            'approval_role_id': sub_approval_flow_settings_entity.current_approval_flow_node_id.operation_role_id.id,

            'approval_result': self.approval_result,

            'approval_opinion': self.approval_opinion,

            'res_model': self.res_model,
            'res_id': self.res_id,

        }
        # 更新审批节点 拿到当前的子环节



        sub_approval_flow_settings_entity.save_approval_flow_info(approval_flow_settings_record_info)



        return {
            'type': 'ir.actions.act_url',
            'name': "Redirect to the Website Projcet Rating Page",
            'target': 'self',
            'url': '/web#active_id=%s&action=approval_kanban_to_detail&model=cowin_project.cowin_project' % (sub_tache_entity.meta_sub_project_id.project_id.id)
        }



    @api.multi
    def button_agree(self):
        if self.status:
            raise UserError(u'已审批完成')
        self.status = True
        self.approval_result = u'True'
        return self.process_approval_flow_info()




    @api.multi
    def button_reject(self):
        if self.status:
            raise UserError(u'已审批完成')
        self.status = True
        self.approval_result = u'False'
        return self.process_approval_flow_info()

    @api.multi
    def button_putoff(self):
        if self.status:
            raise UserError(u'已审批完成')
        self.status = True
        self.approval_result = u'None'
        return self.process_approval_flow_info()




class Common_Dialog(models.Model):

    _name = 'cowin_common.common_dialog'

    warning = fields.Char(string=u'警告!!!', default=u'该审批已经审阅过!!!')


    @api.model
    def show_dialog(self):

        entity = self.create({})

        return {
            'name': entity._name,
            'type': 'ir.actions.act_window',
            'res_model': entity._name,
            'views': [[False, 'form']],
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_id': entity.id,
            'target': 'new',
        }


    def rpc_button_ok(self):

        pass




