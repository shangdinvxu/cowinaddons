# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import re
from odoo import SUPERUSER_ID

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


# 自定义一套 元子工程 员工 审批角色的 表的概念
class Cowin_meta_sub_and_approval_role_and_hr_employee(models.Model):
    _name = 'cowin_project.meta_sub_appro_role_hr_em'
    '''
        这个类进行了一次派生的操作
    '''
    # meta_sub_project_id = fields.Many2one('cowin_project.meat_sub_project', string=u'元子工程' , ondelete="cascade")
    approval_role_id = fields.Many2one('cowin_common.approval_role', string=u'操作角色')
    employee_id = fields.Many2one('hr.employee', string=u'用户')


# 该model的目的在于 所属于的特殊的头衔需要独立存储起来使用, 例如对于风控总监, 管理合伙人,财务专员,投资决策委员会主席
class Cowin_Global_Special_Approval_Role(models.Model):
    _name = 'cowin_project.global_spec_appro_role'

    name = fields.Char(string=u'虚拟角色的名字')
    approval_role_id = fields.Many2one('cowin_common.approval_role', string=u'审批角色', ondelete="cascade")

    count = fields.Integer(string=u'虚拟角色对应的人数')

    count_computed = fields.Char(compute='_compute_count_by_employee_ids')

    employee_ids = fields.Many2many('hr.employee', string=u'相对应的员工')

    count_accumulation = fields.Integer(string=u'员工人数的累加值')

    @api.multi
    def verify_count(self):
        self.ensure_one()
        if self.count_accumulation > self.count:
            raise UserError(u'%s中只允许%s个员工' % (self.name, self.count))

    # @api.depends('employee_ids')
    # def _compute_count_by_employee_ids(self):
    #     print(u'虚拟角色是否已经达到了上限的挑战!!!')
    #     for rec in self:
    #         if len(rec.employee_ids) > rec.count:
    #             raise UserError(u'%s虚拟角色已达到上限!!!' % rec.name)






# 该model对应的意义在于对员工进行分组的操作 即  所属投资决策委员会
class  Cowin_Global_Special_Approval_Group_role(models.Model):
    _name = 'cowin_project.global_spec_appro_group_role'

    name = fields.Char(string=u'角色组名')
    employee_ids = fields.Many2many('hr.employee', string=u'所属的员工')







class Cowin_hr(models.Model):
    _inherit = 'hr.employee'

    label = fields.Selection(AVAILABLE_PRIORITIES, string=u'标签', index=True, default=AVAILABLE_PRIORITIES[0][0])

    compute_is_admin = fields.Boolean(string=u'计算是否属于admin', compute='_compute_is_admin')
    is_admin = fields.Boolean(string=u'是否是admin')

    def _compute_is_admin(self):

        res = self.env.user.id == SUPERUSER_ID
        self.write({
            'is_admin': res,
        })


    backup_person = fields.Char(string=u'备用联系人')
    relation_to_me = fields.Char(string=u'与本人关系')
    identification_id_contract_person = fields.Char(string=u'身份证')
    mobile_phone_backup_contract_person = fields.Char(string=u'联系电话')

    barcode = fields.Char(string=u'员工编码')

    is_add_user = fields.Boolean(string=u'添加登录用户', default=True)
    login_name = fields.Char(string=u'登录邮箱')
    industry = fields.Many2one('cowin_common.cowin_industry', string=u'所属行业')

    identification_id = fields.Char(string='Identification No', groups='base.group_user')
    passport_id = fields.Char('Passport No', groups='base.group_user')

    # 员工与登录角色的关系 理论上 One-2-One关系
    # user_id = fields.Many2one('res.users', string=u'登陆用户')
    #
    # approval_role_ids = fields.Many2many('cowin_common.approval_role', string=u'审批角色')
    sub_meta_pro_approval_settings_role_rel = fields.One2many('cowin_project.meta_sub_appro_role_hr_em', 'employee_id', string=u'审批角色')





    # 新添加的项目的权限的配置
    is_ventilation_control_supervisor = fields.Boolean(string=u'风控总监', default=False)

    is_managing_partner = fields.Boolean(string=u'管理合伙人', default=False)

    is_treasury_attache = fields.Boolean(string=u'财务专员', default=False)

    is_chairman_of_the_investment_decision_committee = fields.Boolean(string=u'投资决策委员会主席', default=False)


    investment_decision_committee_id = fields.Many2one('cowin_project.global_spec_appro_group_role', string=u'所属投资决策委员会')



    _sql_constraints = [
        ('login_name_key', 'UNIQUE (login_name)', 'You can not have two users with the same login !')
    ]


    def kddddk(self):
        print(u'kfjslfjslafjlasfj')
        form_id = self.env.ref('cowin_hr.cowin_hr_form').id

        action = {
            'name': 'kkkkkk',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'views': [[form_id, 'form']],
            'view_type': 'form',
            'view_mode': 'form',
            "res_id": 25,
            'target': 'new',
        }



    def _check_emial_format(self, email):
        print u'开始验证邮箱格式!!!'
        # 验证邮箱格式
        str = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
        return re.match(str, email)


    @api.multi
    def write_special_user_role_or_group(self, vals):
        self.ensure_one()

        spec_appro_role_entities = self.env['cowin_project.global_spec_appro_role'].search([])

        def _inner_filter(name):
            return spec_appro_role_entities.filtered(lambda self: self.name == name)



        # 风控总监
        is_ventilation_control_supervisor = vals.get('is_ventilation_control_supervisor', None)
        if is_ventilation_control_supervisor == True:
            res = _inner_filter(u'风控总监')
            res.verify_count()
            res.write({
                'count_accumulation': res.count_accumulation + 1,
                'employee_ids': [(4, self.id)],
            })

        elif is_ventilation_control_supervisor == False:
            res = _inner_filter(u'风控总监')
            c = res.count_accumulation
            c = c - 1
            if c <= 1:
                c = 1

            res.write({
                'count_accumulation': c,
                'employee_ids': [(3, self.id)],
            })

            self.detach_self_from_project(role_name=u'风控总监')
        else:
            pass



        # 管理合伙人
        is_managing_partner = vals.get('is_managing_partner', None)
        if is_managing_partner == True:

            res = _inner_filter(u'管理合伙人')
            res.verify_count()
            res.write({
                'count_accumulation': res.count_accumulation + 1,
                'employee_ids': [(4, self.id)],
            })

        elif is_managing_partner == False:

            res = _inner_filter(u'管理合伙人')
            c = res.count_accumulation
            c = c - 1
            if c <= 1:
                c = 1

            res.write({
                'count_accumulation': c,
                'employee_ids': [(3, self.id)],
            })

            self.detach_self_from_project(role_name=u'管理合伙人')

        else:
            pass


        # 财务专员
        is_treasury_attache = vals.get('is_treasury_attache', None)
        if is_treasury_attache == True:
            res = _inner_filter(u'财务专员')
            res.verify_count()
            res.write({
                'count_accumulation': res.count_accumulation + 1,
                'employee_ids': [(4, self.id)],
            })
        elif is_treasury_attache == False:
            res = _inner_filter(u'财务专员')
            c = res.count_accumulation
            c = c - 1
            if c <= 1:
                c = 1

            res.write({
                'count_accumulation': c,
                'employee_ids': [(3, self.id)],
            })

            self.detach_self_from_project(role_name=u'财务专员')

        else:
            pass



        # 投资决策委员会主席
        is_chairman_of_the_investment_decision_committee = vals.get('is_chairman_of_the_investment_decision_committee', None)
        if is_chairman_of_the_investment_decision_committee == True:
            res = _inner_filter(u'投资决策委员会主席')
            res.verify_count()
            res.write({
                'count_accumulation': res.count_accumulation + 1,
                'employee_ids': [(4, self.id)],
            })

        elif is_chairman_of_the_investment_decision_committee == False:
            res = _inner_filter(u'投资决策委员会主席')
            c = res.count_accumulation
            c = c - 1
            if c <= 1:
                c = 1

            res.write({
                'count_accumulation': c,
                'employee_ids': [(3, self.id)],
            })

            self.detach_self_from_project(role_name=u'投资决策委员会主席')

        else:
            pass






        if self.investment_decision_committee_id:
            self.investment_decision_committee_id.write({
                'employee_ids': [(4, self.id)],
            })





    def detach_self_from_project(self, role_name=None):
        # if self.env.user.has
        if self.env.user.id != SUPERUSER_ID:
            raise UserError(u'必须要是admin才能操作')

        project_entities = self.env['cowin_project.cowin_project'].search([])
        project_entities.detach_employee_from_project(employee_id=self.id, role_name=role_name)



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
            'lang': 'zh_CN',
            'tz': 'Asia/Shanghai',

            # 'groups_id': [(4, self.env.ref('cowin_project.cowin_project_group_rule').id)],
            'groups_id': [(4, self.env.ref('cowin_project.cowin_project_menu_group').id),
                          # (4, self.env.ref('hr.group_hr_user').id),
                          (4, self.env.ref('base.group_user').id),
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


        res_hr.write_special_user_role_or_group(vals)
        return res_hr
    
    @api.multi
    def unlink(self):
        self.ensure_one()

        if self.user_id:
            self.user_id.unlink()
            
        return super(Cowin_hr, self).unlink()
        



    @api.multi
    def write(self, vals):
        if not vals.get('investment_decision_committee_id'):

            self.investment_decision_committee_id.write({
                'employee_ids': [(3, self.id)],
            })

        if vals.get('login_name'):
            login_name_strip = vals.get('login_name').strip()

            if not self._check_emial_format(login_name_strip):
                raise UserError(u'邮箱格式错误!!!')

            self.user_id.write({
                'name': login_name_strip,
                'login': login_name_strip,
                'email': login_name_strip,
            })

            # if login_name_strip and not self.login_name == login_name_strip:
            #     raise UserError(u'目前不支持用户角色改写!!!')

        res = super(Cowin_hr, self).write(vals)
        self.write_special_user_role_or_group(vals)

        return res



    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):

        if view_type == 'form':
            if self.env.user.id == SUPERUSER_ID:
                view_id  = self.env.ref('cowin_hr.cowin_hr_form_admin').id
            else:
                view_id = self.env.ref('cowin_hr.cowin_hr_form').id

        elif view_type == 'kanban':
            if self.env.user.id == SUPERUSER_ID:
                view_id  = self.env.ref('cowin_hr.cowin_hr_kanban_view_employees_for_admin').id
            else:
                view_id = self.env.ref('cowin_hr.cowin_hr_kanban_view_employees').id

        return super(Cowin_hr, self).fields_view_get(view_id, view_type, toolbar, submenu)