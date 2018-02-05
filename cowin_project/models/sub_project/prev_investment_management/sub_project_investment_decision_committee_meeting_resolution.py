# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class Cowin_project_subproject_investment_decision_committee_meeting_resolution(models.Model):

    '''
        投资决策委员会会议决议

    '''
    _inherit = 'cowin_project.base_status'

    _name = 'cowin_project.sub_invest_decision_committee_res'

    # 用于显示环节中的名称
    _rec_name = 'sub_tache_id'

    subproject_id = fields.Many2one('cowin_project.cowin_subproject', ondelete="cascade")
    sub_tache_id = fields.Many2one('cowin_project.subproject_process_tache', string=u'子环节实体')


    # name = fields.Char(related='subproject_id.name', string=u"项目名称")
    # project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    # invest_manager_id = fields.Many2one('hr.employee', related='subproject_id.invest_manager_id', string=u'投资经理')

    name = fields.Char(string=u"项目名称")
    project_number = fields.Char(string=u'项目编号')
    # invest_manager_id = fields.Many2one('hr.employee', string=u'投资经理')
    invest_manager_ids = fields.Many2many('hr.employee', 'committee_res_invest_manager_employee_rel', string=u'投资经理')

    prev_voting_date = fields.Date(string=u'投决会日期')
    prev_voting_result = fields.Char(string=u'投决会结果')

    # ----------  投资基金

    # round_financing_and_foundation_id = fields.Many2one('cowin_project.round_financing_and_foundation',
    #                                                     related='subproject_id.round_financing_and_foundation_id',
    #                                                     string=u'基金轮次实体')
    round_financing_id = fields.Many2one('cowin_common.round_financing', string=u'融资轮次')
    foundation_id = fields.Many2one('cowin_foundation.cowin_foudation', string=u'基金名称')
    the_amount_of_financing = fields.Float(string=u'本次融资金额')
    the_amount_of_investment = fields.Float(string=u'本次投资金额')
    ownership_interest = fields.Float(string=u'股份比例')
    project_valuation = fields.Float(string=u'估值')

    compute_round_financing_and_foundation_id = fields.Char(compute=u'_compute_value')

    # @api.depends('round_financing_id', 'foundation_id', 'the_amount_of_financing', 'the_amount_of_investment',
    #              'ownership_interest', 'trustee_id', 'supervisor_id', 'amount_of_entrusted_loan')
    # def _compute_value(self):
    #     for rec in self:
    #         rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].round_financing_id = rec.round_financing_id
    #         rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].foundation_id = rec.foundation_id
    #         rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].the_amount_of_financing = rec.the_amount_of_financing
    #         rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].the_amount_of_investment = rec.the_amount_of_investment
    #         rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].ownership_interest = rec.ownership_interest
    #         rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].project_valuation = rec.project_valuation
    # #
    #         rec.subproject_id.trustee_id = rec.trustee_id
    #         rec.subproject_id.supervisor_id = rec.supervisor_id
    #         rec.subproject_id.amount_of_entrusted_loan = rec.amount_of_entrusted_loan




    trustee_id = fields.Many2one('hr.employee', string=u'董事')
    supervisor_id = fields.Many2one('hr.employee', string=u'监事')
    amount_of_entrusted_loan = fields.Float(string=u'委托贷款金额')
    chairman_of_investment_decision_committee_ids = fields.Many2many('hr.employee', 'committee_res_chairman_of_investment_decision_employee_rel', string=u'投资决策委员会主席')



    # 用于控制新增按钮的显示的操作的操作,以及投资决策是最终的决议!!!
    is_final_meeting_resolution = fields.Boolean(string=u'是否为最终决议', default=False)

    # 审批实体记录
    sub_pro_approval_flow_settings_record_ids = fields.One2many('cowin_project.sub_approval_flow_settings_record',
                                                                'res_id', string=u'审批记录',
                                                                domain=lambda self: [('res_model', '=', self._name)])


    @api.multi
    def write_date_of_review_to_related_model(self):
        for rec in self:
            # rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].round_financing_id = rec.round_financing_id
            # rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].foundation_id = rec.foundation_id
            rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].the_amount_of_financing = rec.the_amount_of_financing
            rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].the_amount_of_investment = rec.the_amount_of_investment
            rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].ownership_interest = rec.ownership_interest
            rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].project_valuation = rec.project_valuation
            #
            rec.subproject_id.trustee_id = rec.trustee_id
            rec.subproject_id.supervisor_id = rec.supervisor_id
            rec.subproject_id.amount_of_entrusted_loan = rec.amount_of_entrusted_loan


    @api.multi
    def check_special_filed(self):
        self.ensure_one()
        extend_entity = self.env['cowin.project.detail.round'].search([('project_id', '=', self.subproject_id.meta_project_id.project_id.id),
                                                                       ('round_financing_id', '=', self.round_financing_id)])

        if self.the_amount_of_financing != extend_entity.the_amount_of_financing or \
            self.project_valuation != extend_entity.project_valuation:
            raise UserError(u'本次融资金额 和 估值必须为 %s, %s' % (extend_entity.the_amount_of_financing, extend_entity.project_valuation))




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
        res = super(Cowin_project_subproject_investment_decision_committee_meeting_resolution, self).create(vals)

        res.check_special_filed()
        res.write_date_of_review_to_related_model()  # 写入当前子工程的轮次基金实体

        target_sub_tache_entity.write({
            'res_id': res.id,
            # 'is_unlocked': True,
            'view_or_launch': True,
        })

        # 判断 发起过程 是否需要触发下一个子环节
        # target_sub_tache_entity.check_or_not_next_sub_tache()
        target_sub_tache_entity.update_sub_approval_settings()

        # 来解锁投资决策申请环节新增操作!!!
        # meta_sub_project_entity.sub_tache_ids.search([(u'name', u'=', u'投资决策申请')])
        # target = meta_sub_project_entity.sub_tache_ids.filtered(lambda sub: sub.name == u'投资决策申请')
        # target.write({
        #     'once_or_more': True,
        # })

        # 触发下一个依赖子环节处于解锁状态
        # for current_sub_tache_entity in meta_sub_project_entity.sub_tache_ids:
        #     if current_sub_tache_entity.parent_id == target_sub_tache_entity:
        #         current_sub_tache_entity.write({
        #             'is_unlocked': True,
        #         })

        return res




    @api.multi
    def write(self, vals):
        # 重新发起的操作!!!需要鉴别数据
        target_sub_tache_entity = self.sub_tache_id
        if self._context.get('is_launch_again'):
            target_sub_tache_entity.write({
                'is_launch_again': False,
            })

            # 重新发起状态,需要重新写入相关的数据
            self.write_date_of_review_to_related_model()

            # 判断 发起过程 是否需要触发下一个子环节

            target_sub_tache_entity.update_sub_approval_settings()

        # 由于在前端界面中,重写过前端想后端写入的方法,有空值的影响, 尤其是button的操作的影响,所以,我们需要把该问题给过滤掉!!!
        if not vals:
            return True
        self.check_special_filed()
        # self.write_date_of_review_to_related_model()
        result = super(Cowin_project_subproject_investment_decision_committee_meeting_resolution, self).write(vals)
        return result



    def load_and_return_action(self, **kwargs):
        tache_info = kwargs['tache_info']
        # tache_info = self._context['tache']
        meta_sub_project_id = int(tache_info['meta_sub_project_id'])

        meta_sub_project_entity = self.env['cowin_project.meat_sub_project'].browse(meta_sub_project_id)

        sub_project_entity = meta_sub_project_entity.sub_project_ids[0] # 获取子工程实体

        # tem = meta_sub_project_entity.project_id.copy_data()[0]

        res = {}


        common_fileds = [
            'round_financing_id',
            'foundation_id',
            'the_amount_of_financing',
            'the_amount_of_investment',
            'ownership_interest',
            'project_valuation',
        ]

        tem = meta_sub_project_entity.round_financing_and_Foundation_ids[0].read(common_fileds)[0]
        for k, v in tem.iteritems():
            nk = 'default_' + k
            if type(v) is tuple:
                res[nk] = v[0]
            else:
                res[nk] = v


        # target_fileds = ['name', 'project_number', 'invest_manager_id', 'trustee', 'supervisor']
        target_fileds = ['name', 'project_number', 'invest_manager_id', 'prev_voting_date', 'prev_voting_result']

        tem = sub_project_entity.read(target_fileds)[0]
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

        chairman_of_investment_decision_committee_entity = self.env['cowin_common.approval_role'].search(
            [('name', '=', u'投资决策委员会主席')])
        rel_entities = meta_sub_project_entity.sub_meta_pro_approval_settings_role_rel & chairman_of_investment_decision_committee_entity.sub_meta_pro_approval_settings_role_rel
        res['default_chairman_of_investment_decision_committee_ids'] = [(6, 0, [rel.employee_id.id for rel in rel_entities])]

        t_name = self._name + '_form_no_button'
        view_id = self.env.ref(t_name).id

        return {
            'name': tache_info['name'],
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
