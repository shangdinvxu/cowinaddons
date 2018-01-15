# -*- coding: utf-8 -*-

from odoo import models, fields, api
class Cowin_project_subproject_conference_resolutions(models.Model):
    '''
        投资决策委员会会议表决票
    '''
    _inherit = 'cowin_project.base_status'

    _name = 'cowin_project.sub_conference_resolutions'

    # subproject_id = fields.Many2one('cowin_project.cowin_subproject', ondelete="cascade")

    sub_prv_poll_status_id = fields.Many2one('cowin_project.sub_prv_poll_status', string=u'投票状态实体', ondelete="cascade")
    sub_tache_id = fields.Many2one('cowin_project.subproject_process_tache', string=u'子环节实体')


    # name = fields.Char(related='subproject_id.name', string=u"项目名称")
    # project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    # invest_manager_id = fields.Many2one('hr.employee', related='subproject_id.invest_manager_id', string=u'投资经理')

    name = fields.Char(string=u"项目名称")
    project_number = fields.Char(string=u'项目编号')
    # invest_manager_id = fields.Many2one('hr.employee', string=u'投资经理')
    invest_manager_ids = fields.Many2many('hr.employee', string=u'投资经理')

    # ----------  投资基金
    round_financing_and_foundation_id = fields.Many2one('cowin_project.round_financing_and_foundation',
                                                        related='subproject_id.round_financing_and_foundation_id',
                                                        string=u'基金轮次实体')
    round_financing_id = fields.Many2one('cowin_common.round_financing', string=u'融资轮次')
    foundation_id = fields.Many2one('cowin_foundation.cowin_foudation', string=u'基金名称')
    the_amount_of_financing = fields.Float(string=u'本次融资金额')
    the_amount_of_investment = fields.Float(string=u'本次投资金额')
    ownership_interest = fields.Integer(string=u'股份比例')
    # ----------

    voting_committee = fields.Date(string=u'投决会日期')

    members_of_voting_committee_ids = fields.Many2many('hr.employee', string=u'投决会委员')

    voting_opinion = fields.Text(string=u'表决意见')

    voter_id = fields.Many2one('hr.employee', string=u'表决人')

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
        vals['sub_tache_id'] = sub_tache_id
        res = super(Cowin_project_subproject_conference_resolutions, self).create(vals)
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

        return res



    @api.multi
    def write(self, vals):
        res = super(Cowin_project_subproject_conference_resolutions, self).write(vals)
        target_sub_tache_entity = self.sub_tache_id

        if self.inner_or_outer_status == 1:
            target_sub_tache_entity.write({
                'is_launch_again': False,
            })

            # 判断 发起过程 是否需要触发下一个子环节
            # target_sub_tache_entity.check_or_not_next_sub_tache()
            target_sub_tache_entity.update_sub_approval_settings()

        return res

    def load_and_return_action(self, **kwargs):
        tache_info = kwargs['tache_info']
        # tache_info = self._context['tache']
        meta_sub_project_id = int(tache_info['meta_sub_project_id'])

        meta_sub_project_entity = self.env['cowin_project.meat_sub_project'].browse(meta_sub_project_id)

        sub_project_entity = meta_sub_project_entity.sub_project_ids[0]  # 获取子工程实体

        # tem = meta_sub_project_entity.project_id.copy_data()[0]

        common_fileds = [
            'round_financing_id',
            'foundation_id',
            'the_amount_of_financing',
            'the_amount_of_investment',
            'ownership_interest',
        ]

        common_fileds.extend(['name', 'project_number', 'invest_manager_id'])

        tem = sub_project_entity.read(common_fileds)[0]

        res = {}

        for k, v in tem.iteritems():
            nk = 'default_' + k
            if type(v) is tuple:
                res[nk] = v[0]
            else:
                res[nk] = v

        # 默认的投资经理的数据我们需要去自定义添加
        invest_manager_entity = self.env['cowin_common.approval_role'].search([('name', '=', u'投资经理')])
        rel_entities = meta_sub_project_entity.sub_meta_pro_approval_settings_role_rel & invest_manager_entity.sub_meta_pro_approval_settings_role_rel

        res['default_invest_manager_ids'] = [(6, 0, [rel.employee_id.id for rel in rel_entities])]

        investment_decision_committee_entity = self.env['cowin_common.approval_role'].search([('name', '=', u'投资决策委员')])
        rel_entities = meta_sub_project_entity.sub_meta_pro_approval_settings_role_rel & investment_decision_committee_entity.sub_meta_pro_approval_settings_role_rel
        res['default_members_of_voting_committee_ids'] = [(6, 0, [rel.employee_id.id for rel in rel_entities])]


        # 默认情况下 一对一
        res['default_voter_id'] = self.env.user.employee_ids[0].id
        return {
            'name': self._name,
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'views': [[False, 'form']],
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_id': self.id,
            'target': 'new',
            'context': res,
        }