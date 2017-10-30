# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.modules.module import get_module_resource
from odoo import tools


class Cowin_project(models.Model):
    _name = 'cowin_project.cowin_project'

    @api.model
    def _default_image(self):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    # 关联到settings中,把该字段看成配置选项的操作
    process_id = fields.Many2one('cowin_settings.process', ondelete="cascade", required=True)

    image = fields.Binary("LOGO", default=_default_image, attachment=True,
                          help="This field holds the image used as photo for the cowin_project, limited to 1024x1024px.")

    name = fields.Char(string=u"项目名称", required=True)

    project_number = fields.Char(string=u'项目编号',
                                 defualt=lambda self: self.env['ir.sequence'].next_by_code('cowin_project.order'))
    project_source = fields.Selection([(1, u'朋友介绍'), (2, u'企业自荐')],
                              string=u'项目来源', required=True)
    project_source_note = fields.Char(string=u'项目来源备注')
    invest_manager = fields.Many2one('hr.employee', string=u'投资经理')

    # investment_fund = fields.One2many('xxxx.xxxx', 'rrrr_id', string=u'投资基金')
    investment_fund = fields.Char(string=u'投资基金')
    round_financing = fields.Selection([(1, u'天使轮'), (2, u'A轮'), (3, u'B轮'), (4, u'C轮')],
                              string=u'融资轮次', required=True, default=1)
    round_money = fields.Float(string=u'本次融资额')

    project_company_profile = fields.Text(string=u'项目公司概况')
    project_appraisal = fields.Text(string=u'项目评价')
    project_note = fields.Text(string=u'备注')
    industry = fields.Many2one('cowin_project.cowin_common', string=u'所属行业')
    stage = fields.Selection([(1, u'种子期'), (2, u'成长早期'), (3, u'成长期'), (4, u'成熟期')], string=u'所属阶段')
    production = fields.Text(string=u'产品')
    registered_address = fields.Char(string=u'注册地')
    peration_place = fields.Char(string=u'运营地')
    founding_time = fields.Date(string=u'成立时间')
    contract_person = fields.Char(string=u'联系人')
    contract_phone = fields.Char(string=u'联系电话')
    contract_email = fields.Char(string=u'Email')
    # attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=lambda self: [('res_model', '=', self._name)],
    #                                  auto_join=True, string=u"附件")

    attachment_ids = fields.Many2many('ir.attachment', string=u"附件")

    # displayed_image_id = fields.Many2one('ir.attachment', domain="[('res_model', '=', 'project.task'), ('res_id', '=', id), ('mimetype', 'ilike', 'image')]", string='Displayed Image')

    attachment_note = fields.Char(string=u'附件说明')



    #
    # @api.model
    # def create(self, vals):
    #     if not vals.get('project_number'):
    #         vals['project_number'] = self.env['ir.sequence'].next_by_code('cowin_project.order')
    #
    #     return super(Cowin_project, self).create(vals)


    # 获得每个project的xiang详细信息
    def _get_info(self):
        return {'id': self.id,
                'name': self.name,
                'process_id': self.process_id.id
                }


    # 通过rpc调用,把详细的信息传递到前端以便于显示操作
    def rpc_get_info(self):
        return self._get_info()