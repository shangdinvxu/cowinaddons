# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import re

AVAILABLE_PRIORITIES = [
    ('0', 'badly'),
    ('1', 'Low'),
    ('2', 'Normal'),
    ('3', 'High'),
    ('4', 'Very High'),
    ('5', 'top level'),
]




# 构建员工与登陆用户之间的关系  理论上 one 2 one
class Res_users_inherit(models.Model):
    _inherit = 'res.users'

#
    employee_ids = fields.One2many('hr.employee', 'user_id', string=u'员工')
#
#
#
# # 构建员工与审批角色之间的关系 理论上 many 2 many
class Cowin_common_approval_role_inherit(models.Model):
    _inherit = 'cowin_common.approval_role'

    # meta_sub_project_id = fields.Many2one('cowin_project.meat_sub_project', string=u'元子工程')
    # employee_ids = fields.Many2many('hr.employee', string=u'员工')

    sub_meta_pro_approval_settings_role_rel = fields.One2many('cowin_project.meta_sub_appro_role_hr_em', 'approval_role_id', string=u'员工')


#
class Cowin_meta_sub_and_approval_role_and_hr_employee(models.Model):
    _name = 'cowin_project.meta_sub_appro_role_hr_em'
    '''
        这个类进行了一次派生的操作
    '''
    # meta_sub_project_id = fields.Many2one('cowin_project.meat_sub_project', string=u'元子工程' , ondelete="cascade")
    approval_role_id = fields.Many2one('cowin_common.approval_role', string=u'操作角色')
    employee_id = fields.Many2one('hr.employee', string=u'用户')



class Cowin_hr(models.Model):
    _inherit = 'hr.employee'

    label = fields.Selection(AVAILABLE_PRIORITIES, string=u'标签', index=True, default=AVAILABLE_PRIORITIES[0][0])


    backup_person = fields.Char(string=u'备用联系人')
    relation_to_me = fields.Char(string=u'与本人关系')
    identification_id_contract_person = fields.Char(string=u'身份证')
    mobile_phone_backup_contract_person = fields.Char(string=u'联系电话')

    barcode = fields.Char(string=u'员工编码')

    is_add_user = fields.Boolean(string=u'添加登陆用户', default=True)
    login_name = fields.Char(string=u'邮箱')
    industry = fields.Many2one('cowin_common.cowin_industry', string=u'所属行业')

    # 员工与登录角色的关系 理论上 One-2-One关系
    # user_id = fields.Many2one('res.users', string=u'登陆用户')
    #
    # approval_role_ids = fields.Many2many('cowin_common.approval_role', string=u'审批角色')
    sub_meta_pro_approval_settings_role_rel = fields.One2many('cowin_project.meta_sub_appro_role_hr_em', 'employee_id', string=u'审批角色')


    _sql_constraints = [
        ('login_name_key', 'UNIQUE (login_name)', 'You can not have two users with the same login !')
    ]


    def _check_emial_format(self, email):
        print u'开始验证邮箱格式!!!'
        # 验证邮箱格式
        str = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
        return re.match(str, email)




    @api.model
    def create(self, vals):
        if not vals.get('barcode'):
            vals['barcode'] = self.env['ir.sequence'].next_by_code('cowin_hr.order')

        if vals.get('user_id'):  # 这种情况下是在xml中配置了amdmin所对应的员工用户!!!
            return super(Cowin_hr, self).create(vals)

        login_name = vals.get('login_name')

        login_name = login_name and login_name.strip()
        if not (login_name):
            raise UserError(u'登录名不是为空,或者登陆名不能都是空字符串!!!')

        if not self._check_emial_format(login_name):
            raise UserError(u'邮箱格式错误!!!')

        if self.env['res.users'].search([('name', '=', login_name)]):
            print u'该用户已经被添加在其中!!,我们不需要再去做添加的操作了!!'
            # return UserWarning(u'该用户已经存在!!!')

            raise UserError(u'该用户已经存在!!!')

        '''
            手动的方式来创建员工和用户之间一对一的关系!!!
        '''

        user_entity = self.env['res.users'].create({
            'name': login_name,
            'login': login_name,
            'email': login_name,
            # 'groups_id': [(4, self.env.ref('cowin_project.cowin_project_group_rule').id)],
            'groups_id': [(4, self.env.ref('cowin_project.cowin_project_menu_group').id),
                          (4, self.env.ref('hr.group_hr_user').id),
                          # (4, self.env.ref('cowin_project.cowin_project_group').id),]})
                          ]})

        # 设定初始的密码
        pass_wizard = self.env['change.password.wizard'].create({})

        pass_wizard_user = self.env['change.password.user'].create({
            'wizard_id': pass_wizard.id,
            'user_id': user_entity.id,
            'new_passwd': '123456'
        })

        pass_wizard.change_password_button()

        # 创建当前的hr.employee实例
        vals['user_id'] = user_entity.id
        res_hr = super(Cowin_hr, self).create(vals)

        return res_hr



    @api.multi
    def write(self, vals):
        print(type(self))
        print u'开始进入到write方法中开始去执行的操作!!!'
        print self.login_name
        if vals.get('login_name'):
            login_name_strip = vals.get('login_name').strip()

            if not self._check_emial_format(login_name_strip):
                raise UserError(u'邮箱格式错误!!!')

            if login_name_strip and not self.login_name == login_name_strip:
                raise UserError(u'目前不支持用户角色改写!!!')

        res = super(Cowin_hr, self).write(vals)
        return res



