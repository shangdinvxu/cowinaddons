# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.modules.module import get_module_resource
from odoo import tools


# 项目立项  构建小项目

class Cowin_project_subproject(models.Model):
    _name = 'cowin_project.cowin_subproject'

    '''
        项目立项
    '''


    @api.model
    def _default_image(self):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    # 关联到settings中,把该字段看成配置选项的操作
    # project_id = fields.Many2one('cowin_project.cowin_project', ondelete="cascade")
    meta_sub_project_id = fields.Many2one('cowin_project.meat_sub_project', string=u'元子工程实例' , ondelete="cascade")

    # # 这个字段仅仅是为了让程序设计更加的完备性!!!
    # subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    # 关联到自环节表(缓解状态表中)
    # sub_process_tache_status_id = fields.One2many('cowin_project.subproject_process_tache', "sub_project_id")

    examine_and_verify = fields.Char(string=u'审核校验', default=u'未开始审核')


    image = fields.Binary("LOGO", default=_default_image, attachment=True,
                        help="This field holds the image used as photo for the cowin_project, limited to 1024x1024px.")

    name = fields.Char(string=u"项目名称")


    project_number = fields.Char(string=u'项目编号')
    project_source = fields.Selection([(1, u'朋友介绍'), (2, u'企业自荐')],
                              string=u'项目来源', required=True)
    project_source_note = fields.Char(string=u'项目来源备注')
    invest_manager = fields.Many2one('hr.employee', string=u'投资经理')


    # ----------  投资基金
    round_financing_and_foundation_id = fields.Many2one('cowin_project.round_financing_and_foundation', string=u'基金轮次')

    round_financing_id = fields.Many2one('cowin_common.round_financing',
                                         related='round_financing_and_foundation_id.round_financing_id', string=u'轮次')

    foundation_id = fields.Many2one('cowin_foundation.cowin_foudation',
                                    related='round_financing_and_foundation_id.foundation_id', string=u'基金')

    the_amount_of_financing = fields.Float(
                                        related='round_financing_and_foundation_id.the_amount_of_financing', string=u'本次融资额')

    the_amount_of_investment = fields.Float(
                                    related='round_financing_and_foundation_id.the_amount_of_investment', string=u'本次投资金额')
    ownership_interest = fields.Float(
                            related='round_financing_and_foundation_id.ownership_interest',string=u'股份比例')
    # ---------------


    project_company_profile = fields.Text(string=u'项目公司概况')
    project_appraisal = fields.Text(string=u'项目评价')
    project_note = fields.Text(string=u'备注')
    industry = fields.Many2one('cowin_common.cowin_industry', string=u'所属行业')
    stage = fields.Selection([(1, u'种子期'), (2, u'成长早期'), (3, u'成长期'), (4, u'成熟期')], string=u'所属阶段', default=1)
    production = fields.Text(string=u'产品')
    registered_address = fields.Char(string=u'注册地')
    peration_place = fields.Char(string=u'运营地')
    founding_time = fields.Date(string=u'成立时间')
    contract_person = fields.Char(string=u'联系人')
    contract_phone = fields.Char(string=u'联系电话')
    contract_email = fields.Char(string=u'Email')

    attachment_ids = fields.Many2many('ir.attachment', string=u"附件")


    attachment_note = fields.Char(string=u'附件说明')


    @api.model
    def create(self, vals):

        tache = self._context['tache']

        meta_sub_project_id = int(tache['meta_sub_project_id'])

        vals['meta_sub_project_id'] = meta_sub_project_id

        sub_tache_id = int(tache['sub_tache_id'])

        sub_tache = self.env['cowin_project.subproject_process_tache'].browse(sub_tache_id)

        sub_project = super(Cowin_project_subproject, self).create(vals)
        sub_tache.write({
            'res_id': sub_project.id,
            'is_unlocked': True,
            'view_or_launch': True,
        })

        return sub_project


