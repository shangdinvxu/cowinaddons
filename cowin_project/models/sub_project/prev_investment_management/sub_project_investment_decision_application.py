# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Cowin_project_subproject_investment_decision_application(models.Model):

    '''
        投资决策申请
    '''
    _inherit = 'cowin_project.base_status'

    _name = 'cowin_project.sub_invest_decision_app'

    # 用于显示环节中的名称
    _rec_name = 'sub_tache_id'

    subproject_id = fields.Many2one('cowin_project.cowin_subproject', ondelete="cascade")
    sub_tache_id = fields.Many2one('cowin_project.subproject_process_tache', string=u'子环节实体')

    date_of_review = fields.Date(string=u'尽调审核日期')


    # name = fields.Char(related='subproject_id.name', string=u"项目名称")
    # project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    # invest_manager_id = fields.Many2one('hr.employee', related='subproject_id.invest_manager_id', string=u'投资经理')

    name = fields.Char(string=u"项目名称")
    project_number = fields.Char(string=u'项目编号')
    # invest_manager_id = fields.Many2one('hr.employee', string=u'投资经理')
    invest_manager_ids = fields.Many2many('hr.employee', string=u'投资经理')

    # ----------  投资基金
    # 这条数据目前没有用,只是有xml依赖,所以放在这里
    # round_financing_id = fields.Many2one('cowin_common.round_financing',
    #                                      related='subproject_id.round_financing_id', string=u'轮次')

    round_financing_and_foundation_id = fields.Many2one('cowin_project.round_financing_and_foundation',
                                                        related='subproject_id.round_financing_and_foundation_id', string=u'基金轮次实体')
    round_financing_id = fields.Many2one('cowin_common.round_financing', string=u'融资轮次')
    foundation_id = fields.Many2one('cowin_foundation.cowin_foundation', string=u'基金名称')
    the_amount_of_financing = fields.Float(string=u'本次融资金额')
    the_amount_of_investment = fields.Float(string=u'本次投资金额')
    ownership_interest = fields.Float(string=u'股份比例')
    project_valuation = fields.Float(string=u'估值')

    # 审批实体记录
    sub_pro_approval_flow_settings_record_ids = fields.One2many('cowin_project.sub_approval_flow_settings_record',
                                                                'res_id', string=u'审批记录',
                                                                domain=lambda self: [('res_model', '=', self._name)])

    compute_round_financing_and_foundation_id = fields.Char(compute=u'_compute_value')

    # @api.depends('round_financing_id', 'foundation_id', 'the_amount_of_financing', 'the_amount_of_investment',
    #              'ownership_interest')
    # def _compute_value(self):
    #     for rec in self:
    #         rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].round_financing_id = rec.round_financing_id
    #         rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].foundation_id = rec.foundation_id
    #         rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].the_amount_of_financing = rec.the_amount_of_financing
    #         rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].the_amount_of_investment = rec.the_amount_of_investment
    #         rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].ownership_interest = rec.ownership_interest
    #         rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].project_valuation = rec.project_valuation



    # foundation_id = fields.Many2one('cowin_foundation.cowin_foundation',
    #                                 related='subproject_id.foundation_id', string=u'基金')
    #
    # the_amount_of_financing = fields.Float(
    #     related='subproject_id.the_amount_of_financing', string=u'本次融资额')
    #
    # the_amount_of_investment = fields.Float(
    #     related='subproject_id.the_amount_of_investment', string=u'本次投资金额')
    # ownership_interest = fields.Integer(
    #     related='subproject_id.ownership_interest', string=u'股份比例')



    # ---------------

    company_investment_role = fields.Selection([(1, u'单一投资人'), (2, u'主导投资人'), (3, u'跟投')],
                                               string=u'本公司的投资角色')

    # decision_file_list = fields.Many2many('ir.attachment', string=u'决策文件清单')
    decision_file_list = fields.Many2many('ir.attachment', 'sub_invest_decision_app_attachment_rel', string=u'决策文件清单')

    investment_decision_Committee_held_time = fields.Date(string=u'投资决策委员会召开时间')

    # 把一些依赖的字段写入到子工程之中
    @api.multi
    def write_date_of_review_to_related_model(self):
        for rec in self:
            rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].the_amount_of_financing = rec.the_amount_of_financing
            rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].the_amount_of_investment = rec.the_amount_of_investment
            rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].ownership_interest = rec.ownership_interest
            rec.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].project_valuation = rec.project_valuation

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
        res = super(Cowin_project_subproject_investment_decision_application, self).create(vals)
        res.write_date_of_review_to_related_model() #  写入----> 轮次基金实体
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




        # partner_ids = [rel_entity.approval_role.employee_id.user_id.partner_id.id for rel_entity in self.subproject_id.meta_sub_project_id.sub_meta_pro_approval_settings_role_rel
        #      if rel_entity.approval_role.name == u'投资决策委员会']
        # channel_entity = self.env['mail.channel'].create({
        #     'name': u'投决策申请通道 %s' % self.id,
        #     "public": "public",
        # })
        #
        # sub_project_name = res.subproject_id.meta_sub_project_id.sub_project_ids[0].name
        # round_financing_name = res.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].round_financing_id.name
        # foundation_name = res.subproject_id.meta_sub_project_id.round_financing_and_Foundation_ids[0].foundation_id.name
        #
        # sub_project_name = sub_project_name if sub_project_name else u''
        # round_financing_name = round_financing_name if round_financing_name else u'暂无轮次'
        # foundation_name = foundation_name if foundation_name else u'暂无基金'
        #
        # info_first = u'%s/%s/%s\n' % (sub_project_name, round_financing_name, foundation_name)
        # channel_entity.message_post(info_first + u'您有一项[投资决策申请]待审批',
        #             message_type = 'comment', subtype = 'mail.mt_comment')

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

        # self.write_date_of_review_to_related_model()
        res = super(Cowin_project_subproject_investment_decision_application, self).write(vals)

        return res

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


        target_fileds = ['name', 'project_number', 'invest_manager_id', 'date_of_review']

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