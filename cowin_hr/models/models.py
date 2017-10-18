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


class Cowin_hr(models.Model):
    _inherit = 'hr.employee'

    label = fields.Selection(AVAILABLE_PRIORITIES, string=u'标签', index=True, default=AVAILABLE_PRIORITIES[0][0])


    backup_person = fields.Char(string=u'备用联系人')
    relation_to_me = fields.Char(string=u'与本人关系')
    identification_id_contract_person = fields.Char(string=u'身份证')
    mobile_phone_backup_contract_person = fields.Char(string=u'联系电话')

    barcode = fields.Char(string=u'员工编码')

    # is_add_user = fields.Boolean(string=u'添加登陆用户', default=False, compute='_compute_login_name_active')
    is_add_user = fields.Boolean(string=u'添加登陆用户', default=True)
    login_name = fields.Char(string=u'邮箱')

    title = fields.Many2one(related=u'user_id.title')

    _sql_constraints = [
        ('login_key', 'UNIQUE (login_name)', 'You can not have two users with the same login !')
    ]
    # @api.multi
    # def _compute_login_name_active(self):
    #     self.ensure_one()
    #     print u'开始切换开关!!!'
    #     # self.login_name.readonly = True


    def _check_emial_format(self, email):
        print u'开始验证邮箱格式!!!'
        # 验证邮箱格式
        str = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
        # if not re.match(str, email):
        #     raise UserError(u'邮箱格式错误!!!')
        #
        return re.match(str, email)

    @api.model
    def create(self, vals):
        if not vals.get('barcode'):
            vals['barcode'] = self.env['ir.sequence'].next_by_code('cowin_hr.order')


        # 创建当前的hr.employee实例
        res_hr = super(Cowin_hr, self).create(vals)

        login_name_strip = vals.get('login_name').strip()
        # # 开始对外键进行设置
        if login_name_strip:

            if not self._check_emial_format(login_name_strip):
                raise UserError(u'邮箱格式错误!!!')


            # 这样的命名的规则是从字段的命名规则来考虑

            if self.env['res.users'].search([('name', '=', login_name_strip)]).ids:
                print u'该用户已经被添加在其中!!,我们不需要再去做添加的操作了!!'
                # return UserWarning(u'该用户已经存在!!!')

                raise UserError(u'该用户已经存在!!!')

            user_id = self.env['res.users'].create({
                'name': login_name_strip,
                'login':login_name_strip,
                'email': login_name_strip
            })

            pass_wizard = self.env['change.password.wizard'].create({})

            pass_wizard_user = self.env['change.password.user'].create({
                'wizard_id': pass_wizard.id,
                'user_id': user_id.id,
                'new_passwd': '123456'
            })

            pass_wizard.change_password_button()

            # 把邮箱存储到与res.users相关的res.partnter中

            res_hr.user_id = user_id.id
            res_hr.address_home_id = user_id.partner_id.id
        return res_hr


    @api.multi
    def write(self, vals):
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



