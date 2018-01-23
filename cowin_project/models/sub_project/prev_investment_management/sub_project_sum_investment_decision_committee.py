# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class Cowin_project_subproject_sum_investment_decision_committee(models.Model):
    '''
        投资决策委员会会议纪要
    '''
    _inherit = 'cowin_project.base_status'

    _name = 'cowin_project.sub_sum_invest_decision_committee'

    subproject_id = fields.Many2one('cowin_project.cowin_subproject', ondelete="cascade")
    sub_tache_id = fields.Many2one('cowin_project.subproject_process_tache', string=u'子环节实体')


    # name = fields.Char(related='subproject_id.name', string=u"项目名称")
    # project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    # invest_manager_id = fields.Many2one('hr.employee', related='subproject_id.invest_manager_id', string=u'投资经理')
    invest_manager_ids = fields.Many2many('hr.employee', 'decision_committee_invest_manager_employee_rel', string=u'投资经理')


    name = fields.Char(string=u"项目名称")
    project_number = fields.Char(string=u'项目编号')
    # invest_manager_id = fields.Many2one('hr.employee', string=u'投资经理')

    voting_committee_date = fields.Date(string=u'投决会日期')

    compute_voting_committee_date = fields.Char(compute=u'_compute_value')

    @api.depends('voting_committee_date')
    def _compute_value(self):
        for rec in self:
            rec.subproject_id.voting_committee_date = self.voting_committee_date



    conference_recorder = fields.Many2one('hr.employee', string=u'会议记录人')
    checker = fields.Many2one('hr.employee', string=u'复核人')
    investment_decision_committee_ids = fields.Many2many('hr.employee', 'decision_committee_investment_decision_committee_employee_rel',  string=u'投资决策委员')

    conference_highlights = fields.Text(string=u'会议要点')



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

        res = super(Cowin_project_subproject_sum_investment_decision_committee, self).create(vals)
        # 手动的操作把数据写入到子工程中!!!

        # 局部数据写入,用以避免与发起状态之间产生的操作!!!
        # res.is_called_by_sth = True

        res.subproject_id.write({
            'inner_or_outer_status': 2,     # write方法 状态发生变化
        })
        res.subproject_id.voting_committee_date = res.voting_committee_date




        if not res.investment_decision_committee_ids:
            raise UserError(u'没有给投资决策委员配置员工信息, 以至于不能进行投票!!!')

        target_sub_tache_entity.write({
            'res_id': res.id,
            # 'is_unlocked': True,
            'view_or_launch': True,
        })

        # 判断 发起过程 是否需要触发下一个子环节
        target_sub_tache_entity.update_sub_approval_settings()

        # target_sub_tache_entity.write_special_vote(prev_or_post_vote=True)







        # 触发下一个依赖子环节处于解锁状态
        # for current_sub_tache_entity in meta_sub_project_entity.sub_tache_ids:
        #     if current_sub_tache_entity.parent_id == target_sub_tache_entity:
        #         current_sub_tache_entity.write({
        #             'is_unlocked': True,
        #         })

        return res

    @api.multi
    def write(self, vals):

        # 由于在前端界面中,冲写过前端想后端写入的方法,有空值的影响,所以,我们需要把该问题给过滤掉!!!
        if not vals:
            return True

        res = super(Cowin_project_subproject_sum_investment_decision_committee, self).write(vals)

        # button在当前的业务逻辑中当前属于审核状态, 分发之后的业务,业务逻辑不同
        if self.button_status == 1 or self.button_status == 2:
            return res
        if not res.investment_decision_committee_ids:
            raise UserError(u'没有给投资决策委员配置员工信息, 以至于不能进行投票!!!')
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
        ]

        common_fileds.extend(['name', 'project_number'])

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
        res['default_investment_decision_committee_ids'] = [(6, 0, [rel.employee_id.id for rel in rel_entities])]

        t_name = self._name + '_form_no_button'
        view_id = self.env.ref(t_name).id

        return {
            'name': self._name,
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'views': [[view_id, 'form']],
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_id': self.id,
            'target': 'new',
            'context': res,
        }