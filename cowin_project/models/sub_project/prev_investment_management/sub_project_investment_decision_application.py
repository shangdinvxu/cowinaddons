# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Cowin_project_subproject_investment_decision_application(models.Model):

    '''
        投资决策申请
    '''

    _name = 'cowin_project.sub_invest_decision_app'

    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    invest_manager_id = fields.Many2one('hr.employee', related='subproject_id.invest_manager_id', string=u'投资经理')

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

    company_investment_role = fields.Selection([(1, u'单一投资人'), (2, u'主导投资人'), (3, u'跟投')],
                                               string=u'本公司的投资角色')

    decision_file_list = fields.Many2many('ir.attachment', string=u'决策文件清单')

    investment_decision_Committee_held_time = fields.Date(string=u'投资决策委员会召开时间')


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
        res = super(Cowin_project_subproject_investment_decision_application, self).create(vals)
        target_sub_tache_entity.write({
            'res_id': res.id,
            # 'is_unlocked': True,
            'view_or_launch': True,
        })

        # 判断 发起过程 是否需要触发下一个子环节
        # target_sub_tache_entity.check_or_not_next_sub_tache()
        target_sub_tache_entity.update_sub_approval_settings()

        # 触发下一个依赖子环节处于解锁状态
        # for current_sub_tache_entity in meta_sub_project_entity.sub_tache_ids:
        #     if current_sub_tache_entity.parent_id == target_sub_tache_entity:
        #         current_sub_tache_entity.write({
        #             'is_unlocked': True,
        #         })


        # 发送投资决策通知!!!
        # for rel_entity in self.subproject_id.meta_sub_project_id.sub_meta_pro_approval_settings_role_rel:
        #     pass


        partner_ids = [rel_entity.approval_role.employee_id.user_id.partner_id.id for rel_entity in self.subproject_id.meta_sub_project_id.sub_meta_pro_approval_settings_role_rel
             if rel_entity.approval_role.name == u'投资决策委员会']
        channel_entity = self.env['mail.channel'].create({
            'name': u'投决策申请通道 %s' % self.id,
            "public": "public",
        })

        sub_project_name = res.subproject_id.meta_sub_project_id.sub_project_ids[0].name
        round_financing_name = res.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].round_financing_id.name
        foundation_name = res.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].foundation_id.name

        sub_project_name = sub_project_name if sub_project_name else u''
        round_financing_name = round_financing_name if round_financing_name else u'暂无轮次'
        foundation_name = foundation_name if foundation_name else u'暂无基金'

        info_first = u'%s/%s/%s\n' % (sub_project_name, round_financing_name, foundation_name)
        channel_entity.message_post(info_first + u'您有一项[投资决策申请]待审批',
                    message_type = 'comment', subtype = 'mail.mt_comment')

        return res



    @api.multi
    def write(self, vals):
        res = super(Cowin_project_subproject_investment_decision_application, self).write(vals)
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
        # target_sub_tache_entity.check_or_not_next_sub_tache()
        target_sub_tache_entity.update_sub_approval_settings()

        return res