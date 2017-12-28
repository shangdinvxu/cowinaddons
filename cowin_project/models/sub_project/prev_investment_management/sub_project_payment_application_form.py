# -*- coding: utf-8 -*-
from odoo import models, fields, api
class Cowin_project_subproject_payment_application_form(models.Model):
    '''
        付款申请表
    '''

    _name = 'cowin_project.sub_payment_app_form'

    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    invest_manager_id = fields.Many2one('hr.employee', related='subproject_id.invest_manager_id', string=u'投资经理')

    date_of_application = fields.Date(string=u'申请日期')


    list_of_examination_and_approval_documents = fields.Many2many('ir.attachment', string=u'审批文件')

    monetary_unit = fields.Char(string=u'货币单位')
    the_payment_amount = fields.Float(string=u'本期付款金额')
    total_investment = fields.Float(string=u'公司投资总额')

    number_of_periods = fields.Integer(string=u'付款期数')
    accumulated_payment_amount = fields.Float(string=u'累计付款金额')
    payment_amount = fields.Float(string=u'未付金额')

    payee_name = fields.Char(string=u'收款人名称')
    account_number = fields.Char(string=u'收款账号')
    bank_of_deposit = fields.Char(string=u'开户银行')
    funds_provided = fields.Char(string=u'资金来源')

    # ----------  投资基金
    round_financing_id = fields.Many2one('cowin_common.round_financing',
                                         related='subproject_id.round_financing_id', string=u'轮次')

    foundation_id = fields.Many2one('cowin_foundation.cowin_foudation',
                                    related='subproject_id.foundation_id', string=u'基金')

    the_amount_of_financing = fields.Float(
        related='subproject_id.the_amount_of_financing', string=u'本次融资额')

    the_amount_of_investment = fields.Float(
        related='subproject_id.the_amount_of_investment', string=u'本次投资金额')
    ownership_interest = fields.Integer(
        related='subproject_id.ownership_interest', string=u'股份比例')
    # ---------------
    payment_account = fields.Char(string=u'付款账号')


    @api.model
    def create(self, vals):
        tache_info = self._context['tache']

        # sub_project_id = int(tache_info['sub_project_id'])

        sub_tache_id = int(tache_info['sub_tache_id'])
        meta_sub_project_id = int(tache_info['meta_sub_project_id'])
        meta_sub_project_entity = self.env['cowin_project.meat_sub_project'].browse(meta_sub_project_id)

        sub_project_id = meta_sub_project_entity.sub_project_ids.id

        target_sub_tache_entity = meta_sub_project_entity.sub_tache_ids.browse(sub_tache_id)

        vals['subproject_id'] = sub_project_id
        res = super(Cowin_project_subproject_payment_application_form, self).create(vals)
        target_sub_tache_entity.write({
            'res_id': res.id,
            # 'is_unlocked': True,
            'view_or_launch': True,
        })

        # 判断 发起过程 是否需要触发下一个子环节
        target_sub_tache_entity.check_or_not_next_sub_tache()


        # 由 '付款申请表来获得投后跟进列表的展现的操作(鼠标点击投后跟进菜单项的时候)!!!'

        project_entity = res.subproject_id.meta_sub_project_id.project_id

        # 类对象中的属性
        project_entity.write({
            'prev_or_post_investment': False,
        })

        return res

    @api.multi
    def write(self, vals):
        res = super(Cowin_project_subproject_payment_application_form, self).write(vals)
        tache_info = self._context['tache']

        meta_sub_project_id = int(tache_info['meta_sub_project_id'])

        # 校验meta_sub_project所对应的子工程只能有一份实体
        meta_sub_project_entity = self.env['cowin_project.meat_sub_project'].browse(meta_sub_project_id)

        sub_tache_id = int(tache_info['sub_tache_id'])

        target_sub_tache_entity = meta_sub_project_entity.sub_tache_ids.browse(sub_tache_id)

        target_sub_tache_entity.write({
            'is_launch_again': False,
        })

        # 判断 发起过程 是否需要触发下一个子环节
        target_sub_tache_entity.check_or_not_next_sub_tache()

        return res


