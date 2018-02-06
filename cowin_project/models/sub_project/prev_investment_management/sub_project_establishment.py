# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.modules.module import get_module_resource
from odoo import tools
from odoo.exceptions import UserError

# 项目立项  构建小项目

class Cowin_project_subproject(models.Model):
    _inherit = 'cowin_project.base_status'

    _name = 'cowin_project.cowin_subproject'

    '''
        项目立项
    '''
    # 用于显示环节中的名称
    _rec_name = 'sub_tache_id'

    @api.model
    def _default_image(self):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    # 关联到settings中,把该字段看成配置选项的操作
    # project_id = fields.Many2one('cowin_project.cowin_project', ondelete="cascade")
    meta_sub_project_id = fields.Many2one('cowin_project.meat_sub_project', string=u'元子工程实例' , ondelete="cascade")

    sub_tache_id = fields.Many2one('cowin_project.subproject_process_tache', string=u'子环节实体')


    # # 这个字段仅仅是为了让程序设计更加的完备性!!!
    # subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    # 关联到自环节表(缓解状态表中)
    # sub_process_tache_status_id = fields.One2many('cowin_project.subproject_process_tache', "sub_project_id")

    examine_and_verify = fields.Char(string=u'审核校验', default=u'未开始审核')


    image = fields.Binary("LOGO", default=_default_image, attachment=True,
                        help="This field holds the image used as photo for the cowin_project, limited to 1024x1024px.")

    name = fields.Char(string=u"项目名称")
    project_number = fields.Char(string=u'项目编号')
    # project_source = fields.Selection([(1, u'朋友介绍'), (2, u'企业自荐')], string=u'项目来源')
    project_source = fields.Many2one('cowin_common.project_source', string=u'项目来源')
    project_source_note = fields.Char(string=u'项目来源备注')
    invest_manager_id = fields.Many2one('hr.employee', string=u'投资经理')
    invest_manager_ids = fields.Many2many('hr.employee', string=u'投资经理')

    # ----- 某些字段可能在某个条件下是可编辑的,可能咋其他的条件下是可编辑的
    # is_some_files_edit_or_not = fields.Boolean(string=u'该条件可能在某些情况下是变化的', default=True)


    # ----------  投资基金
    round_financing_and_foundation_id = fields.Many2one('cowin_project.round_financing_and_foundation',
                                                        string=u'基金轮次实体')
    round_financing_id = fields.Many2one('cowin_common.round_financing', string=u'融资轮次')


    # 由于轮次的使用需要依赖于外部的投资的介入,所以需要做一些指定的操作
    @api.onchange('round_financing_id')
    def _onchange_round_financing_id(self):

        if self._context.get('rec_new_found_round_info'):
            project_id = self._context.get('rec_new_found_round_info')['project_id']

            tem = self.env['cowin.project.detail.round'].search([('project_id', '=', project_id),
                                                       ('round_financing_id', '=', self.round_financing_id.id)])
        elif self._context.get('project_info'):
            project_id = self._context['project_info']['project_id']
            tem = self.env['cowin.project.detail.round'].search(
                [('project_id', '=', project_id),
                 ('round_financing_id', '=', self.round_financing_id.id)])

        else:
            tem = self.env['cowin.project.detail.round'].search([('project_id', '=', self.meta_sub_project_id.project_id.id),
                                                                 ('round_financing_id', '=',self.round_financing_id.id)])

        self.the_amount_of_financing = tem.the_amount_of_financing
        self.project_valuation = tem.project_valuation

        # if tem:
        #     self.is_some_files_edit_or_not = True
        #
        # else:
        #     self.is_some_files_edit_or_not = False




    foundation_id = fields.Many2one('cowin_foundation.cowin_foudation', string=u'基金名称')
    the_amount_of_financing = fields.Float(string=u'本次融资金额')
    the_amount_of_investment = fields.Float(string=u'本次投资金额')
    ownership_interest = fields.Float(string=u'股份比例')
    project_valuation = fields.Float(string=u'估值')

    compute_round_financing_and_foundation_id = fields.Char(compute=u'_compute_value')


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

    # attachment_ids = fields.Many2many('ir.attachment', string=u"附件")
    attachment_ids = fields.Many2many('ir.attachment', 'cowin_subproject_attachment_rel', string=u"附件")


    attachment_note = fields.Char(string=u'附件说明')

    # 审批实体记录
    sub_pro_approval_flow_settings_record_ids = fields.One2many('cowin_project.sub_approval_flow_settings_record',
                                                                'res_id', string=u'审批记录',
                                                                domain=lambda self: [('res_model', '=', self._name)])

    # 立项意见书 表中投决会日期的依赖的字段
    date_of_project = fields.Date(string=u'立项日期')

    # 投资决策委员会会议纪要 依赖的字段
    # voting_committee = fields.Date(string=u'投决会日期')



    # 投资决策委员会会议决议 这张字表需要使用该字段的一次影像!!!f

    trustee_id = fields.Many2one('hr.employee', string=u'董事')
    supervisor_id = fields.Many2one('hr.employee', string=u'监事')

    # 投决会决议 这张表使用的该字段的一次影像!!!
    amount_of_entrusted_loan = fields.Float(string=u'委托贷款金额')



    # 投资决策委员会会议纪要 表中投决会日期的依赖的字段
    prev_voting_date = fields.Date(string=u'投决会日期')

    # 项目退出会议纪要 表中投决会日期的依赖的字段
    post_voting_date = fields.Date(string=u'项目退出会议日期')


    # 投资决策委员会 表中的会议结果需要依赖的字段   ----投前环节
    prev_voting_result = fields.Char(string=u'投资决策委员会会议决议结果')

    # 尽调报告审核通过的日期!!!
    date_of_review = fields.Date(string=u'尽调审核日期')



    # 项目退出会议表决票 需要写入的投票的结果 --- 投后环节
    post_voting_result = fields.Char(string=u'项目退出会议结果')


    # 把一些依赖的字段写入到子工程之中
    @api.multi
    def write_date_of_review_to_related_model(self):
        for rec in self:
            rec.meta_sub_project_id.round_financing_and_Foundation_ids[0].round_financing_id = rec.round_financing_id
            rec.meta_sub_project_id.round_financing_and_Foundation_ids[0].foundation_id = rec.foundation_id
            rec.meta_sub_project_id.round_financing_and_Foundation_ids[0].the_amount_of_financing = rec.the_amount_of_financing
            rec.meta_sub_project_id.round_financing_and_Foundation_ids[0].the_amount_of_investment = rec.the_amount_of_investment
            rec.meta_sub_project_id.round_financing_and_Foundation_ids[0].ownership_interest = rec.ownership_interest
            rec.meta_sub_project_id.round_financing_and_Foundation_ids[0].project_valuation = rec.project_valuation


    def unlink_blank_sub_project(self):
        self.meta_sub_project_id.search(
            [('project_id', '=', self.meta_sub_project_id.project_id), ('is_on_use', '=', False)]).unlink()




    @api.model
    def create(self, vals):

        # 判断的理由在于前端界面新增基金时,不同的操作的接口

        sub_project_entity = None
        if self._context.get('tache'):

            tache_info = self._context['tache']

            meta_sub_project_id = int(tache_info['meta_sub_project_id'])

            # 校验meta_sub_project所对应的子工程只能有一份实体
            meta_sub_project_entity = self.env['cowin_project.meat_sub_project'].browse(meta_sub_project_id)
            if len(meta_sub_project_entity.sub_project_ids) > 1:
                raise UserError(u'每个元子工程只能有一份实体!!!')

            sub_tache_id = int(tache_info['sub_tache_id'])
            vals['meta_sub_project_id'] = meta_sub_project_id
            vals['sub_tache_id'] = sub_tache_id

            sub_project_entity = super(Cowin_project_subproject, self).create(vals)

        elif self._context.get('rec_new_found_round_info'):

            # 前端界面新增的接口的操作使用案例

            info = self._context['rec_new_found_round_info']

            project_id = info['project_id']

            name = 'cowin_project.cowin_subproject'

            meta_sub_pro_entity = self.meta_sub_project_id.create({
                'project_id': project_id,
            })



            meta_sub_pro_entity.round_financing_and_Foundation_ids.create({
                'meta_sub_project_id': meta_sub_pro_entity.id,
            })

            sub_tache_entity = meta_sub_pro_entity.sub_tache_ids.filtered(
                lambda e: e.tache_id.model_id.model_name == name)

            vals['meta_sub_project_id'] = meta_sub_pro_entity.id
            vals['sub_tache_id'] = sub_tache_entity.id



            sub_project_entity = super(Cowin_project_subproject, self).create(vals)

            sub_project_entity.meta_sub_project_id.project_id.write({
                'whether_new_meta_sub_project_or_not': False,
            })
            sub_tache_entity.write({
                'res_id': sub_project_entity.id,
                'is_unlocked': True,
            })

        else:
            raise UserError(u'创建子工程出错!!!')

            # sub_project = super(Cowin_project_subproject, self).create(vals)

        #  外部,不需要tache中内容的运行




        sub_project_entity.write_date_of_review_to_related_model()  # 将数据写入到指定的位置!!!

        target_sub_tache_entity = sub_project_entity.sub_tache_id


        target_sub_tache_entity.write({
            'res_id': sub_project_entity.id,
            'view_or_launch': True,
        })

        # 判断 发起过程 是否需要触发下一个子环节
        target_sub_tache_entity.update_sub_approval_settings()


        return sub_project_entity


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
        res = super(Cowin_project_subproject, self).write(vals)

        return res



    def load_and_return_action(self, **kwargs):
        tache_info = kwargs['tache_info']
        # tache_info = self._context['tache']
        meta_sub_project_id = int(tache_info['meta_sub_project_id'])

        meta_sub_project_entity = self.env['cowin_project.meat_sub_project'].browse(meta_sub_project_id)

        tem = meta_sub_project_entity.project_id.copy_data()[0]
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

        # res['default_meta_sub_project_id'] = meta_sub_project_id
        # res['default_project_id'] = meta_sub_project_entity.project_id.id
        res['project_info'] = {
            'project_id': meta_sub_project_entity.project_id.id,
        }


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





