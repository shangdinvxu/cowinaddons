# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.modules.module import get_module_resource
from odoo import tools
from odoo.exceptions import UserError
from odoo import SUPERUSER_ID
from odoo.tools.mail import html_sanitize, html2plaintext

import json

# # 审批角色
# class Cowin_common_approval_role_project_inherited(models.Model):
#     _inherit = 'cowin_common.approval_role'
#
#     project_approval_role_ids = fields.Many2many('cowin_project.project_approval_role', 'cowin_approval_role_cowin_project_rel',  string=u'工程主角色')

# class innner_status_for_project(models.Model):
#     _name = 'cowin_project.innner_status'
#
#     prev_or_post_investment = fields.Boolean(default=True, string=u'投前/投后')


class Cowin_project(models.Model):

    _name = 'cowin_project.cowin_project'
    _order = "create_date DESC"

    # 这些公有的字段用于投前,投后区别
    created = False
    # prev_or_post_investment = True

    # innner_status_id = fields.Many2one('cowin_project.innner_status', string=u'主工程内部状态,标志区分投前/投后')

    @classmethod
    def update_created(cls, ture_or_false):
        # 此方法一般需要用类名的方式来访问
        cls.created = ture_or_false

    @classmethod
    def get_created(cls):
        return cls.created

    @api.model
    def _default_image(self):
        image_path = get_module_resource('web', 'static/src/img', 'placeholder.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    # 关联到settings中,把该字段看成配置选项的操作
    process_id = fields.Many2one('cowin_project.process', ondelete="cascade")
    # sub_project_ids = fields.One2many('cowin_project.cowin_subproject', 'project_id', string=u'子工程')
    meta_sub_project_ids = fields.One2many('cowin_project.meat_sub_project', 'project_id', string=u'元子工程')

    examine_and_verify = fields.Char(string=u'审核校验', default=u'未开始审核')


    image = fields.Binary("LOGO", default=_default_image, attachment=True,
                          help="This field holds the image used as photo for the cowin_project, limited to 1024x1024px.")

    name = fields.Char(string=u"项目名称")

    # project_number = fields.Char(string=u'项目编号',
    #                              defualt=lambda self: self.env['ir.sequence'].next_by_code('cowin_project.order'))
    # project_source = fields.Selection([(1, u'朋友介绍'), (2, u'企业自荐')],string=u'项目来源')
    project_source = fields.Many2one('cowin_common.project_source', string=u'项目来源')


    project_source_note = fields.Char(string=u'项目来源备注')
    # invest_manager = fields.Many2one('hr.employee', string=u'投资经理')

    round_financing = fields.Many2one('cowin_common.round_financing', string=u'融资轮次')
    round_money = fields.Float(string=u'本次融资额')

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
    attachment_ids = fields.Many2many('ir.attachment', 'cowin_project_attachment_rel', string=u"附件")

    prev_or_post_investment = fields.Boolean(string=u'投前/投后', default=True)


    # main_approval_role_ids = fields.One2many('cowin_project.project_approval_role', 'project_id', string=u'工程主角色')


    attachment_note = fields.Char(string=u'附件说明')

    # # 投前 获取当前主工程所有的发起人角色
    # prev_approval_flow_launch_roles_ids = fields.Many2many('cowin_common.approval_role', string=u'投前发起角色')
    #
    # # 投前 获取当期主工程所有的审批角色
    # prev_approval_flow_role_ids = fields.Many2many('cowin_common.approval_role', string=u'投前审批角色')
    #
    # # 投后 获取当前主工程所有的发起人角色
    # post_approval_flow_launch_roles_ids = fields.Many2many('cowin_common.approval_role', string=u'投后发起角色')
    #
    # # 投后 获取当期主工程所有的审批角色
    # post_approval_flow_role_ids = fields.Many2many('cowin_common.approval_role', string=u'投后审批角色')

    whether_new_meta_sub_project_or_not = fields.Boolean(string=u'是否用于创建元子工程', default=False)

    # 添加数据版本号,用来校验数据是否在存储的过程之中已经发生了变化
    data_version = fields.Integer(string=u'数据版本号', default=0)
    is_admin_user = fields.Boolean(string=u'是否是超级用户', default=False)
    is_admin_user_computed = fields.Boolean(compute='_compute_is_admin_user')

    def _compute_is_admin_user(self):

        if self.env.user.id == SUPERUSER_ID:
            self.write({
                'is_admin_user': True,
            })
        else:

            self.write({
                'is_admin_user': False,
            })


    # 考虑到设计上的规则性,每个工程的创建需要做很多的事情
    @api.model
    def create(self, vals):

        # 1, 创建工程配置实例
        process = None
        # if not vals.get('project_number'):
        #     vals['project_number'] = self.env['ir.sequence'].next_by_code('cowin_project.order')

        if not vals.get('process_id'):
            meta_setting_entities = self.env['cowin_settings.process'].search(['|',
                      ('category', '=', 'init_preinvestment'), ('category', '=', 'init_postinvestment')])

            meta_settings_info = {}

            prev_meta_settings_entity = self.env['cowin_settings.process'].search([('category', '=', 'init_previnvestment')])
            post_meta_settings_entity = self.env['cowin_settings.process'].search([('category', '=', 'init_postinvestment')])

            # odoo这些精炼的方法让笔者用起来感觉确实很方便, 默认情况下投前流程只能怪的阶段中 prev_or_post_investment 是为True
            # post_meta_settings_entity.stage_ids.write({'prev_or_post_investment': False})


            meta_settings_info = prev_meta_settings_entity.copy_custom()
            for stage_info in meta_settings_info['stage_ids']:
                stage_info['prev_or_post_investment'] = True

            post_meta_stage_infos = post_meta_settings_entity.copy_custom()['stage_ids']

            for stage_info in post_meta_stage_infos:
                stage_info['prev_or_post_investment'] = False

            meta_settings_info['stage_ids'].extend(post_meta_stage_infos)
            # 每次创建的实例 都要从数据
            # process = self.env['cowin_project.process'].create_process_info(meta_setting_entity.copy_custom(),
            #                                                                 meta_setting_entity.id)



            # 注意,这个self只是代表着一个空的project实体,方便以后的使用!!!
            process = self.process_id.create_process_info(meta_settings_info, vals['name'])

            vals['process_id'] = process.id


        project = super(Cowin_project, self).create(vals)

        # 把当前的主工程和虚拟角色进行绑定操作!!!
        # prev_approval_flow_launch_roles_entities, prev_approval_flow_roles_entities,  \
        #     post_approval_flow_launch_roles_entities, post_approval_flow_roles_entities  = process.approval_launch_roles_flow_roles()

        # project.main_approval_role_ids.create({
        #     'project_id': project.id,
        #     'status': 1,
        #     'approval_role_ids': [(6, 0, map(lambda x: x.id, prev_approval_flow_launch_roles_entities))],
        # })
        #
        # project.main_approval_role_ids.create({
        #     'project_id': project.id,
        #     'status': 2,
        #     'approval_role_ids': [(6, 0, map(lambda x: x.id, prev_approval_flow_roles_entities))],
        # })
        #
        # project.main_approval_role_ids.create({
        #     'project_id': project.id,
        #     'status': 3,
        #     'approval_role_ids': [(6, 0, map(lambda x: x.id, post_approval_flow_launch_roles_entities))],
        # })
        #
        # project.main_approval_role_ids.create({
        #     'project_id': project.id,
        #     'status': 4,
        #     'approval_role_ids': [(6, 0, map(lambda x: x.id, post_approval_flow_roles_entities))],
        # })




        #  更改解锁条件
        #  修改这个需求的作用在于对之后的环节进行处理
        for tache in process.get_all_tache_entities():

            if tache.model_id.model_name == self._name:
                # 主工程的实例id需要根据思路写入res_id之中
                # 主工程所在的环节的解锁条件需要开启
                tache.write({
                    'res_id': project.id,
                    # 代表  解锁中
                    'is_unlocked': True,
                    'view_or_launch': True,
                    'once_or_more': False,
                })

                break



        # 1-1 默认创建 元子工程实例
        # 注意self为 空,即没需要的实体,空的实体
        meta_sub_project = self.meta_sub_project_ids.create({
            'project_id': project.id,
            # 这类情况下,需要设定为可以使用的状态!!!
            # 'is_on_use': True,
        })



        # #
        # self.env['cowin_project.round_financing_and_foundation'].create({
        #     'meta_sub_project_id': meta_sub_project.id,
        #     # 很显然,这种情况下是只能是为空的,因为是第一次的操作!!!
        #     'sub_invest_decision_committee_res_id': None,
        # })
        #
        #
        # # 1-2 默认创建该元子工程实例一个基金轮次实例
        meta_sub_project.round_financing_and_Foundation_ids.create({
            'meta_sub_project_id': meta_sub_project.id,
            # 很显然,这种情况下是只能是为空的,因为是第一次的操作!!!
            'sub_invest_decision_committee_res_id': None,
        })

        # type(self).created = True
        # setattr(type(self.env[self._name]), 'created', True)
        type(self.env[self._name]).update_created(True)
        return project





    # 由于project表有许多其他的表动态关联到该project之中,所以,此方法的
    # 目的在于动态的查找出该project所对应的one2many的所有的对象实体,
    # 由于是动态的操作模型,所以该project不方便使用one2many的操作
    def _check_view_status(self, foudation_id, round_financing):
        '''

        :param foudation_id:   基金 id
        :param round_financing:  基金所在的某个轮次
        :return:
        '''
        if not foudation_id or not round_financing:
            return None

        # 拿到该项目中配置信息的所有的环节数据
        taches = self.process_id.get_all_taches()

        t = None
        temp = []
        for tache in taches:
            if tache.model_name:
                # 当前表和model_name表属于同一张表,由于设计上的缺陷!!!
                if tache.model_name == self._name:
                    t = self.id
                else:

                    # 某个基金的stage(实例)/(记录)
                    foudation = self.env['cowin_foudation.cowin_foudation'].browse(int(foudation_id))
                    foudation_stage_id = foudation.get_round_financing(round_financing).id
                    t = self.env[tache.model_name].search([('foudation_stage_id', '=', foudation_stage_id)]).id
            else:
                t = False
            temp.append({'tache_id': tache,
                         'model_name': tache.model_name,
                         'res_id': t
                         })

        return temp



    # 主工程配置的环节需要和子工程的配置的环节进行关联处理
    def process_settings2(self, meta_sub_project_id, prev_or_post_investment=True):
        '''

        :param meta_sub_project_id: 子工程实例id
        :return:
        '''

        # 1 获取原始的配置信息
        process_info = self.process_id.get_info(prev_or_post_investment)




        # 2 获取指定的一个元子工程信息
        meta_sub_project_entity = None
        # 代表着第一次默认选择第一个来显示,当然,如果存在的情况下
        # 返回给客户的时候页面需要默认显示的一条轮次基金数据
        if not meta_sub_project_id:
            meta_sub_project_entity = self.meta_sub_project_ids

            # 第一条数据存在
            if meta_sub_project_entity:
                meta_sub_project_entity = meta_sub_project_entity[0]

        else:

            meta_sub_project_entity = self.meta_sub_project_ids.browse(meta_sub_project_id)


        sub_project_info = meta_sub_project_entity.sub_project_ids[0].copy_data()[0] if meta_sub_project_entity.sub_project_ids else {}



        # 3 元子工程信息中存在的字环节与原始环节进行合并配置

        sub_tache_entities = meta_sub_project_entity.get_sub_taches()
        tache_infos = [tache_info for stage_info in process_info['stage_ids']
                  for tache_info in stage_info['tache_ids']]

        # 处理由于前端界面 新增操作而产生的新的子环节的数据


        # 处理主工程有关的主环节信息
        for tache_info in tache_infos:

            if self.process_id.get_all_tache_entities()[0].browse(tache_info['id']).model_id.model_name == self._name:
                tache_info['approval_status'] = {}
                tache_info['approval_status']['status_id'] = -1
                tache_info['approval_status']['status_name'] = u''
                tache_info['approval_status']['approval_view_or_launch'] = None
                tache_info['approval_status']['sub_approval_flow_settings_id'] = -1

                break


        # 处理元子工程对应的子环节的信息
        # 1, 装配阶段信息

        stages = []
        for stage_info in process_info['stage_ids']:

            res = True
            for tache_info in stage_info['tache_ids']:
                if tache_info['model_name'] == self._name:
                    res = False

            if res:
                stages.append(stage_info)


        for stage_info in stages:
            # 从新渲染装配
            stage_info['tache_ids'] = []

            for sub_tache_entity in sub_tache_entities:
                if sub_tache_entity.tache_id.stage_id.id == stage_info['id']:

                    tache_info = {}

                    # brother_sub_tache_entities = meta_sub_project_entity.sub_tache_ids & sub_tache_entity.tache_id.tache_status_ids
                    #
                    # if len(brother_sub_tache_entities) == 1:
                    #     once_or_more = brother_sub_tache_entities.once_or_more
                    #     tache_info['once_or_more'] = once_or_more
                    #
                    # elif len(brother_sub_tache_entities) > 1 and sub_tache_entity == brother_sub_tache_entities[0]:
                    #     if brother_sub_tache_entities[-1].sub_pro_approval_flow_settings_ids.is_success():
                    #         once_or_more = brother_sub_tache_entities[0].once_or_more
                    #
                    #         tache_info['once_or_more'] = once_or_more



                    tache_info['id'] = sub_tache_entity.tache_id.id
                    tache_info['sub_tache_id'] = sub_tache_entity.id

                    tache_info['name'] = sub_tache_entity.name
                    tache_info['parent_id'] = sub_tache_entity.id
                    # parent_id 就是解锁条件
                    tache_info['is_unlocked'] = sub_tache_entity.is_unlocked
                    # 需要考虑到环节的父节点可能没有
                    # tmp_tache['is_unlocked'] = True if not tache.parent_id else tache.parent_id.is_unlocked
                    # tmp_tache['is_unlocked'] = tache.is_unlocked
                    tache_info['description'] = sub_tache_entity.tache_id.description
                    tache_info['state'] = sub_tache_entity.tache_id.state
                    tache_info['once_or_more'] = sub_tache_entity.once_or_more

                    tache_info['view_or_launch'] = sub_tache_entity.view_or_launch
                    tache_info['is_launch_again'] = sub_tache_entity.is_launch_again
                    tache_info['res_id'] = sub_tache_entity.res_id

                    # tmp_tache['res_id'] = tache.res_id
                    tache_info['model_name'] = sub_tache_entity.tache_id.model_id.model_name
                    tache_info['stage_id'] = sub_tache_entity.tache_id.stage_id.id

                    tache_info['meta_sub_project_id'] = meta_sub_project_entity.id
                    tache_info['sub_project_id'] = meta_sub_project_entity.sub_project_ids.id

                    # 当前的子审批流实体
                    # target_sub_approval_flow_entity = sub_tache_entity.tache_id.approval_flow_settings_ids.sub_approval_flow_settings_ids & \
                    #                                   meta_sub_project_entity.sub_approval_flow_settings_ids

                    # 理论上每个子环节都有自己一个子审批实体
                    target_sub_approval_flow_entity = sub_tache_entity.sub_pro_approval_flow_settings_ids

                    tache_info['approval_status'] = {}
                    tache_info['approval_status']['status_id'] = target_sub_approval_flow_entity.status
                    tache_info['approval_status']['sub_approval_flow_settings_id'] = target_sub_approval_flow_entity.id
                    status = target_sub_approval_flow_entity.status
                    info = ''

                    is_target_role = self.is_target_role(target_sub_approval_flow_entity)

                    # True 代表着审核状态
                    approval_view_or_launch = None
                    if status == 1:

                        name = target_sub_approval_flow_entity.current_approval_flow_node_id.operation_role_id.name
                        # 由xxx发起
                        info = u'由%s发起' % name

                        if tache_info['is_launch_again']:
                            # 有过暂缓的状态
                            info = u'暂缓'
                            approval_view_or_launch = False
                        # is_target_role = self.is_target_role(target_sub_approval_flow_entity)
                        # 当前用户是否属于某个角色!!!
                        if is_target_role:
                            # approval_view_or_launch = False
                            pass
                        else:
                            if not tache_info['view_or_launch']:
                                tache_info['view_or_launch'] = None





                    elif status == 2:
                        # 审核中...
                        # 找出当前的审核人
                        name = target_sub_approval_flow_entity.current_approval_flow_node_id.operation_role_id.name
                        info = u'待%s审核' % name

                        tache_info['once_or_more'] = False
                        # 当前用户是否属于某个角色!!!
                        if is_target_role:
                            # approval_view_or_launch = False

                            approval_view_or_launch = True
                        else:
                            approval_view_or_launch = None



                    # elif status == 3:
                    #     # 暂缓(需要从新操作!!!)
                    #     info = u'暂缓'
                    elif status == 4:
                        # 同意
                        info = u'同意'
                        approval_view_or_launch = False

                        if not is_target_role:
                            tache_info['once_or_more'] = False


                    elif status == 5:
                        # 拒绝
                        info = u'拒绝'
                        approval_view_or_launch = False

                    elif status == 6:
                        info = u'投票中...'
                        approval_view_or_launch = None

                    elif status == 7:
                        info = u'同意'
                        approval_view_or_launch = None
                    else:
                        pass

                    tache_info['approval_status']['status_name'] = info
                    tache_info['approval_status']['approval_view_or_launch'] = approval_view_or_launch

                    #  1  <--------------- 需要传递的上下文信息,共享的基金轮次实体
                    tache_info['round_financing_and_foundation'] = {}

                    tache_info['round_financing_and_foundation']['round_financing_and_foundation_id'] = \
                    meta_sub_project_entity. \
                        round_financing_and_Foundation_ids[0].id

                    tache_info['round_financing_and_foundation']['foundation_id'] = meta_sub_project_entity. \
                        round_financing_and_Foundation_ids[0].foundation_id.id

                    tache_info['round_financing_and_foundation']['round_financing_id'] = meta_sub_project_entity. \
                        round_financing_and_Foundation_ids[0].round_financing_id.id

                    tache_info['round_financing_and_foundation']['the_amount_of_investment'] = meta_sub_project_entity. \
                        round_financing_and_Foundation_ids[0].the_amount_of_investment

                    tache_info['round_financing_and_foundation']['ownership_interest'] = meta_sub_project_entity. \
                        round_financing_and_Foundation_ids[0].ownership_interest

                    tache_info['round_financing_and_foundation']['the_amount_of_financing'] = meta_sub_project_entity. \
                        round_financing_and_Foundation_ids[0].the_amount_of_financing

                    # -------------->

                    # 2 ------->   共享的子工程实例  可能为空,不过odoo特性很良好
                    # 运用odoo的特性可以非常好的使用空实体的问题
                    tache_info['sub_project'] = {}
                    tache_info['sub_project']['sub_project_id'] = meta_sub_project_entity.sub_project_ids.id
                    tache_info['sub_project']['name'] = meta_sub_project_entity.sub_project_ids.name
                    tache_info['sub_project']['project_number'] = meta_sub_project_entity.sub_project_ids.project_number
                    tache_info['sub_project'][
                        'invest_manager_id'] = meta_sub_project_entity.sub_project_ids.invest_manager_id.id



                    stage_info['tache_ids'].append(tache_info)




        return (process_info['stage_ids'], sub_project_info)


    def is_target_role(self, target_sub_approval_flow_entity):
        meta_sub_project_entity = target_sub_approval_flow_entity.meta_sub_project_id
        current_operation_role_entity = target_sub_approval_flow_entity.current_approval_flow_node_id.operation_role_id

        # 当前虚拟角色所属的员工
        sub_approval_settings_role_ids1 = current_operation_role_entity.sub_meta_pro_approval_settings_role_rel

        # 需要考虑到是不同的元子工程来配置角色,获得到时虚拟角色和员工之间的M 2 M之间的关系
        approval_role_and_employee_ids = meta_sub_project_entity.sub_meta_pro_approval_settings_role_rel

        # 当前员工所对应的角色
        tmp = self.env.user.employee_ids
        tmp = tmp if len(tmp) <= 1 else tmp[0]
        sub_approval_settings_role_ids2 = tmp.sub_meta_pro_approval_settings_role_rel
        # 当前用户所对应的员工
        # current_employee = self.env.user.employee_ids

        # current_user_approval_flow_ids = self.env.user.employee_ids.approval_role_ids

        # 接下来要考虑当前用户是否属于某一个虚拟角色
        # if current_approval_flow_entity in current_user_approval_flow_ids:
        if approval_role_and_employee_ids & sub_approval_settings_role_ids1 & sub_approval_settings_role_ids2:
            # if current_employee in employee_ids:
            # 很显然当前用户可以审批
            return True

        # elif:
        #     return self.env.user == SUPERUSER_ID
        else:
            # 很显然不需要去审批,因为没有这个
            return self.env.user.id == SUPERUSER_ID


    # 获得每个project的详细信息
    def _get_info(self, **kwargs):
        tmp = kwargs.get("meta_project_id")
        meta_project_id = 0 if not tmp else int(tmp)
        prev_or_post_investment = kwargs.get('prev_or_post_investment')

        info = self.copy_data()[0]
        info['id'] = self.id
        info['investment_funds'] = self.get_investment_funds()


        # 需要传递数据
        info['process'], info['sub_project_info'] = self.process_settings2(meta_project_id, prev_or_post_investment)
        info['permission_configuration'] = self.rpc_get_permission_configuration()

        return info



    # 获得该项目中投资基金所在的投资轮次, 相当于子工程 sub_project
    def get_investment_funds(self):

        res = []
        count = 0

        # 获得所有的子工程
        meta_sub_projects = self.meta_sub_project_ids

        # 如果没有相应的实例,就直接返回
        if not meta_sub_projects:
            return res

        # 如果有实例的情况
        for meta_sub_pro in meta_sub_projects:
            # 从设计的角度考虑,这里方法只会返回一条基金轮次数据
            round_financing_and_foundation_entity = meta_sub_pro.get_target_financing_and_foundation()

            # 输入 轮次基金id -->  res[i] (i需要的索引)

            found = False
            for i, round_financing_dict in enumerate(res):
                if round_financing_dict.get('round_financing_id') == round_financing_and_foundation_entity.\
                        round_financing_id.id:

                    round_financing_dict['foundation_names'].append({
                        'foundation_id': round_financing_and_foundation_entity.foundation_id.id,
                        'foundation_name': round_financing_and_foundation_entity.foundation_id.name,
                        'meta_sub_project_id': meta_sub_pro.id,
                    })
                    # break 最里面的一层循环
                    found = True
                    break



            if not found:
                res.append({
                    # 轮次
                    'round_financing_id': round_financing_and_foundation_entity.round_financing_id.id,
                    'round_financing_name': round_financing_and_foundation_entity.round_financing_id.name,
                    'foundation_names': [{
                        'foundation_id': round_financing_and_foundation_entity.foundation_id.id,
                        'foundation_name': round_financing_and_foundation_entity.foundation_id.name,
                        'meta_sub_project_id': meta_sub_pro.id,
                    }],
                })

                count += 1


        return res





    # 通过rpc调用,把详细的信息传递到前端以便于显示操作
    def rpc_get_info(self, **kwargs):
        kwargs['prev_or_post_investment'] = True
        return self._get_info(**kwargs)


    # 投后的操作,操作的流程的使用的特性!!!
    def rpc_get_post_info(self, **kwargs):
        kwargs['prev_or_post_investment'] = False
        return self._get_info(**kwargs)

    # 投前新增
    def rpc_new_tache_prev(self, **kwargs):
        meta_sub_project_id = kwargs['meta_sub_project_id']
        sub_tache_ids = kwargs['sub_tache_ids']

        if len(sub_tache_ids) > 1:
            return self.new_four_sub_tache(
                meta_sub_project_id=meta_sub_project_id,
                sub_tache_ids=sub_tache_ids,)

        elif len(sub_tache_ids) == 1:

            return self.new_sub_tache(
                meta_sub_project_id=meta_sub_project_id,
                sub_tache_id=sub_tache_ids[0],)
        else:

            pass



    # 新增(一个)子环节
    def new_sub_tache(self, **kwargs):

        meta_sub_project_id = kwargs['meta_sub_project_id']
        current_sub_tache_id = kwargs['sub_tache_id']

        meta_sub_project_entity = self.meta_sub_project_ids.browse(meta_sub_project_id)
        sub_tache_entity = meta_sub_project_entity.sub_tache_ids.browse(current_sub_tache_id)
        current_tache_entity = sub_tache_entity.tache_id

        # 新增子环节期间,把该子环节 on_or_more 属性设定为False

        sub_tache_entity.write({
            'once_or_more': False,
        })


        # 获取当前子环节所有的兄弟环节
        brother_sub_tache_entities = meta_sub_project_entity.sub_tache_ids & current_tache_entity.tache_status_ids

        # brother_sub_tache_entities = brother_sub_tache_entities

        index = len(brother_sub_tache_entities) + 1
        is_last = True


        for sub_tache_e in meta_sub_project_entity.sub_tache_ids:

            if sub_tache_e.order_parent_id == brother_sub_tache_entities[-1]:

                is_last = False
                    # 新增子环节

                new_sub_tache_entity = brother_sub_tache_entities.create({
                    'name': brother_sub_tache_entities[0].name + ' ' + str(index),
                    'meta_sub_project_id': brother_sub_tache_entities[-1].meta_sub_project_id.id,
                    'tache_id': brother_sub_tache_entities[-1].tache_id.id,
                    'order_parent_id': brother_sub_tache_entities[-1].id,
                    'parent_id': brother_sub_tache_entities[-1].id,
                    'is_unlocked': True,
                })

                sub_tache_e.write({
                    'order_parent_id': new_sub_tache_entity.id,
                })

                break


        if is_last:
            # index = brother_sub_tache_entities[-1].index + 1
            brother_sub_tache_entities.create({
                        'name': brother_sub_tache_entities[0].name + ' ' + str(index),
                        'meta_sub_project_id': brother_sub_tache_entities[-1].meta_sub_project_id.id,
                        'tache_id': brother_sub_tache_entities[-1].tache_id.id,
                        'order_parent_id': brother_sub_tache_entities[-1].id,
                        'parent_id': brother_sub_tache_entities[-1].id,
                        'is_unlocked': True,
                    })

        return self.rpc_get_info(meta_project_id=meta_sub_project_id)

    def new_four_sub_tache(self, **kwargs):
        meta_sub_project_id = kwargs['meta_sub_project_id']
        sub_tache_ids = kwargs['sub_tache_ids']

        meta_sub_project_entity = self.meta_sub_project_ids.browse(meta_sub_project_id)

        to_do_list = []

        sub_tache_entities = meta_sub_project_entity.sub_tache_ids.browse(sub_tache_ids)

        sub_tache_entities[0].write({
            'once_or_more': False,
        })

        # 拿出当前最后的一个依赖的子环节实体
        current_last_sub_tache_entity = None

        for sub_tache_entity in sub_tache_entities:


            current_tache_entity = sub_tache_entity.tache_id


            # 获取当前子环节所有的兄弟环节
            brother_sub_tache_entities = meta_sub_project_entity.sub_tache_ids & current_tache_entity.tache_status_ids

            # 拿出最后的一个依赖
            if sub_tache_entity == sub_tache_entities[-1]:
                current_last_sub_tache_entity = brother_sub_tache_entities[-1]


            # brother_sub_tache_entities = brother_sub_tache_entities

            index = len(brother_sub_tache_entities) + 1

            new_sub_tache_entity = brother_sub_tache_entities.create({
                'name': brother_sub_tache_entities[0].name + ' ' + str(index),
                'meta_sub_project_id': brother_sub_tache_entities[-1].meta_sub_project_id.id,
                'tache_id': brother_sub_tache_entities[-1].tache_id.id,
                # 'order_parent_id': brother_sub_tache_entities[-1].id,
                # 'parent_id': brother_sub_tache_entities[0].id,
                # 'is_unlocked': True,
            })

            # sub_tache_e.write({
            #     'order_parent_id': new_sub_tache_entity.id,
            # })

            to_do_list.append(new_sub_tache_entity)


        # 默认情况下第一个需要解锁
        to_do_list[0].write({
            'is_unlocked': True,
        })

        # # 默认情况下,把第新增条件隐藏
        # to_do_list[0].write({
        #     'once_or_more': False,
        # })

        # 列表逆序,数据写入依赖条件
        revered_to_list = to_do_list[::-1]



        # 默认构建依赖关系
        for i, sub_tache_entity in enumerate(revered_to_list[:-1]):
            sub_tache_entity.write({
                'parent_id': revered_to_list[i+1].id,
                'order_parent_id': revered_to_list[i+1].id,
            })



        to_do_list[0].write({
            'parent_id': current_last_sub_tache_entity.id,
            'order_parent_id': current_last_sub_tache_entity.id,
        })



        remain_tachetities = set(meta_sub_project_entity.sub_tache_ids) - set(to_do_list)




        for sub_tache_e in remain_tachetities:

            if sub_tache_e.order_parent_id == current_last_sub_tache_entity:
                sub_tache_e.write({
                    'order_parent_id': to_do_list[-1].id,
                    'parent_id': to_do_list[-1].id,
                })





        return self.rpc_get_info(meta_project_id=meta_sub_project_id)




    # 投后新增
    def rpc_new_tache_post(self, **kwargs):
        meta_sub_project_id = kwargs['meta_sub_project_id']
        sub_tache_ids = kwargs['sub_tache_ids']

        if len(sub_tache_ids) > 1:
            return self.new_four_sub_tache_post(
                meta_sub_project_id=meta_sub_project_id,
                sub_tache_ids=sub_tache_ids,)

        elif len(sub_tache_ids) == 1:

            return self.new_sub_tache_post(
                meta_sub_project_id=meta_sub_project_id,
                sub_tache_id=sub_tache_ids[0],)
        else:

            pass

    # 新增(一个)子环节
    def new_sub_tache_post(self, **kwargs):

        meta_sub_project_id = kwargs['meta_sub_project_id']
        current_sub_tache_id = kwargs['sub_tache_id']

        meta_sub_project_entity = self.meta_sub_project_ids.browse(meta_sub_project_id)
        sub_tache_entity = meta_sub_project_entity.sub_tache_ids.browse(current_sub_tache_id)

        sub_tache_entity.write({
            'once_or_more': False,
        })

        current_tache_entity = sub_tache_entity.tache_id

        # 获取当前子环节所有的兄弟环节
        brother_sub_tache_entities = meta_sub_project_entity.sub_tache_ids & current_tache_entity.tache_status_ids
        brother_sub_tache_entities.sorted('id')

        # brother_sub_tache_entities = brother_sub_tache_entities

        index = len(brother_sub_tache_entities) + 1
        is_last = True



        for sub_tache_e in meta_sub_project_entity.sub_tache_ids:

            if sub_tache_e.order_parent_id == brother_sub_tache_entities[-1]:
                is_last = False
                # 新增子环节

                new_sub_tache_entity = brother_sub_tache_entities.create({
                    'name': brother_sub_tache_entities[0].name + ' ' + str(index),
                    'meta_sub_project_id': brother_sub_tache_entities[-1].meta_sub_project_id.id,
                    'tache_id': brother_sub_tache_entities[-1].tache_id.id,
                    'order_parent_id': brother_sub_tache_entities[-1].id,
                    'parent_id': brother_sub_tache_entities[-1].id,
                    'is_unlocked': True,
                })

                sub_tache_e.write({
                    'order_parent_id': new_sub_tache_entity.id,

                })

                break


        if is_last:
            # index = brother_sub_tache_entities[-1].index + 1
            brother_sub_tache_entities.create({
                'name': brother_sub_tache_entities[0].name + ' ' + str(index),
                'meta_sub_project_id': brother_sub_tache_entities[-1].meta_sub_project_id.id,
                'tache_id': brother_sub_tache_entities[-1].tache_id.id,
                'order_parent_id': brother_sub_tache_entities[-1].id,
                'parent_id': brother_sub_tache_entities[-1].id,
                'is_unlocked': True,
            })

        return self.rpc_get_post_info(meta_project_id=meta_sub_project_id)


    def new_four_sub_tache_post(self, **kwargs):
        meta_sub_project_id = kwargs['meta_sub_project_id']
        sub_tache_ids = kwargs['sub_tache_ids']

        meta_sub_project_entity = self.meta_sub_project_ids.browse(meta_sub_project_id)

        to_do_list = []

        sub_tache_entities = meta_sub_project_entity.sub_tache_ids.browse(sub_tache_ids)
        sub_tache_entities[0].write({
            'once_or_more': False,
        })
        # 拿出当前最后的一个依赖的子环节实体
        current_last_sub_tache_entity = None


        for sub_tache_entity in sub_tache_entities:

            # sub_tache_entity = meta_sub_project_entity.sub_tache_ids.browse(current_sub_tache_id)
            current_tache_entity = sub_tache_entity.tache_id


            # 获取当前子环节所有的兄弟环节
            brother_sub_tache_entities = meta_sub_project_entity.sub_tache_ids & current_tache_entity.tache_status_ids

            # 拿出最后的一个依赖
            if sub_tache_entity == sub_tache_entities[-1]:
                current_last_sub_tache_entity = brother_sub_tache_entities[-1]
            # brother_sub_tache_entities = brother_sub_tache_entities

            index = len(brother_sub_tache_entities) + 1

            new_sub_tache_entity = brother_sub_tache_entities.create({
                'name': brother_sub_tache_entities[0].name + ' ' + str(index),
                'meta_sub_project_id': brother_sub_tache_entities[-1].meta_sub_project_id.id,
                'tache_id': brother_sub_tache_entities[-1].tache_id.id,
                # 'order_parent_id': brother_sub_tache_entities[-1].id,
                # 'parent_id': brother_sub_tache_entities[0].id,
                # 'is_unlocked': True,
            })

            # sub_tache_e.write({
            #     'order_parent_id': new_sub_tache_entity.id,
            # })

            to_do_list.append(new_sub_tache_entity)


        # 默认情况下第一个需要解锁
        to_do_list[0].write({
            'is_unlocked': True,
        })

        # 默认情况下,把第新增条件隐藏
        # to_do_list[-1].write({
        #     'once_or_more': False,
        # })



        # 列表逆序,数据写入依赖条件
        revered_to_list = to_do_list[::-1]



        # 默认构建依赖关系
        for i, sub_tache_entity in enumerate(revered_to_list[:-1]):
            sub_tache_entity.write({
                'parent_id': revered_to_list[i+1].id,
                'order_parent_id': revered_to_list[i+1].id,
            })



        to_do_list[0].write({
            'parent_id': current_last_sub_tache_entity.id,
            'order_parent_id': current_last_sub_tache_entity.id,
        })



        remain_tachetities = set(meta_sub_project_entity.sub_tache_ids) - set(to_do_list)




        for sub_tache_e in remain_tachetities:

            if sub_tache_e.order_parent_id == current_last_sub_tache_entity:
                sub_tache_e.write({
                    'order_parent_id': to_do_list[-1].id,
                    'parent_id': to_do_list[-1].id,

                })

        return self.rpc_get_post_info(meta_project_id=meta_sub_project_id)















    # 构建审批流,

    # 获取子审批流记录信息
    def rpc_get_approval_flow_info(self, **kwargs):
        tache_info = kwargs.get('tache')
        meta_sub_project_id = tache_info['meta_sub_project_id']
        sub_approval_flow_settings_id = tache_info['sub_approval_flow_settings_id']
        meta_sub_project_entity = self.meta_sub_project_ids.browse(meta_sub_project_id)
        sub_approval_flow_settings_entity = meta_sub_project_entity.sub_approval_flow_settings_ids.browse(sub_approval_flow_settings_id)

        return sub_approval_flow_settings_entity.get_all_sub_aproval_flow_settings_records()









    # 保存子审批流信息
    def rpc_save_approval_flow_info(self, **kwargs):
        tache_info = kwargs.get('tache')
        meta_sub_project_id = tache_info['meta_sub_project_id']
        sub_approval_flow_settings_id = tache_info['sub_approval_flow_settings_id']
        meta_sub_project_entity = self.meta_sub_project_ids.browse(meta_sub_project_id)
        sub_approval_flow_settings_entity = meta_sub_project_entity.sub_approval_flow_settings_ids.browse(sub_approval_flow_settings_id)

        sub_approval_flow_settings_info = tache_info['sub_approval_flow_settings_info']
        status_id = sub_approval_flow_settings_info['status_id']

        if status_id != sub_approval_flow_settings_entity.status:
            raise UserError(u'审批状态发生改变,请刷新界面!!!')

        prev_or_post_investment = kwargs['prev_or_post_investment']


        approval_flow_settings_record_info = kwargs.get('approval_flow_settings_record')

        # 理论上只会有一个员工  审批人
        approval_flow_settings_record_info['approval_person_id'] = self.env.user.employee_ids[0].id

        # 审批角色
        approval_flow_settings_record_info['approval_role_id'] = sub_approval_flow_settings_entity.current_approval_flow_node_id.operation_role_id.id

        # 更新审批节点 拿到当前的子环节

        sub_approval_flow_settings_entity.save_approval_flow_info(approval_flow_settings_record_info)



        # if sub_approval_flow_settings_entity.is_success():
        #
        #     # 触发下一个子环节
        #     current_sub_tache_entity = meta_sub_project_entity.sub_tache_ids.browse(tache_info['sub_tache_id'])
        #
        #     for sub_tache_entity in meta_sub_project_entity.get_sub_taches():
        #         if sub_tache_entity.parent_id == current_sub_tache_entity:
        #             sub_tache_entity.write({
        #                 'is_unlocked': True,
        #                 # 'status': 2,
        #             })
        #
        #
        #             # 在触发下一个子环节过程中,还需要触发下一个子环节所对应的子审批节点信息
        #
        #             sub_approval_flow_settings_entity_next = sub_tache_entity.sub_pro_approval_flow_settings_ids
        #
        #             sub_approval_flow_settings_entity_next.write({
        #                 'status': 2,
        #             })
        #
        #             break


        return self._get_info(meta_project_id=meta_sub_project_id, prev_or_post_investment=prev_or_post_investment)




    # 获取权限配置数据
    def rpc_get_permission_configuration(self):
        res = []
        default_is_full = True

        for meta_sub_pro_entity in self.meta_sub_project_ids:
            tmp = {}
            tmp['meta_sub_pro_id'] = meta_sub_pro_entity.id

            name1 = meta_sub_pro_entity.round_financing_and_Foundation_ids[0].round_financing_id.name
            name1 = name1 if name1 else u'暂无轮次'

            name2 = meta_sub_pro_entity.round_financing_and_Foundation_ids[0].foundation_id.name
            name2 = name2 if name2 else u'暂无基金'

            tmp['foundation_for_rund_financing_info'] = name1 + '-' + name2

            tmp['approval_role_infos'] = []

            approval_role_employee_rel_repr = meta_sub_pro_entity.sub_meta_pro_approval_settings_role_rel[0] if meta_sub_pro_entity.sub_meta_pro_approval_settings_role_rel else meta_sub_pro_entity.sub_meta_pro_approval_settings_role_rel
            approval_role_ids = approval_role_employee_rel_repr.approval_role_id.search([])

            employee_ids = approval_role_employee_rel_repr.employee_id.search([])

            default_is_full = True

            for approval_role_entity in approval_role_ids:
                tmp2 = {}
                tmp2['approval_role_id'] = approval_role_entity.id
                tmp2['approval_role_name'] = approval_role_entity.name

                tmp2['employee_infos'] = [{'employee_id': approval_employee_rel.employee_id.id, 'name': approval_employee_rel.employee_id.name_related}
                    for approval_employee_rel in meta_sub_pro_entity.sub_meta_pro_approval_settings_role_rel if approval_employee_rel.approval_role_id == approval_role_entity]


                if not tmp2['employee_infos']:
                    default_is_full = False


                tmp['approval_role_infos'].append(tmp2)

            tmp['default_is_full'] = default_is_full

            default_is_full = default_is_full and tmp['default_is_full']

            res.append(tmp)


        return {
            'meta_sub_project_infos': res,
            'default_is_full': default_is_full,
            'is_admin': self.env.user.id == SUPERUSER_ID,
            'employee_infos': [{'employee_id': employee_entity.id, 'name': employee_entity.name_related} for employee_entity in employee_ids]
        }


    # 保存权限配置数据
    def rpc_save_permission_configuration(self, **kwargs):

        meta_sub_project_infos = kwargs.get('meta_sub_project_infos')


        for meta_sub_project_info in meta_sub_project_infos:
            meta_sub_project_info[u'is_current_exists'] = False  # 我们之前的数据在前端复制数据的时候,会提前把数据写入,可能有些数据我们并不需要在之后的操作

        # meta_sub_project_entity = self.meta_sub_project_ids.browse(meta_sub_project_id)
        # self._save_permission_configuration(meta_sub_project_entity, meta_sub_project_info)



        for meta_sub_project_entity in self.meta_sub_project_ids:

            for meta_sub_project_info in meta_sub_project_infos:
                if meta_sub_project_info[u'meta_sub_pro_id'] == meta_sub_project_entity.id:

                    self._save_permission_configuration(meta_sub_project_entity, meta_sub_project_info)
                    meta_sub_project_info[u'is_current_exists'] = True
                    break


        # 删除可能之前删除的子工程配置的数据
        for meta_sub_project_entity in self.meta_sub_project_ids:
            for meta_sub_project_info in meta_sub_project_infos:
                if meta_sub_project_info[u'meta_sub_pro_id'] == meta_sub_project_entity.id:
                    if meta_sub_project_info[u'is_current_exists'] == False:
                        # self._save_permission_configuration(meta_sub_project_entity, meta_sub_project_info)
                        meta_sub_project_entity.unlink()
                        break
        #
        return self.rpc_get_permission_configuration()



    def _save_permission_configuration(self, meta_sub_project_entity, meta_sub_project_info):

        current_rel_entities = meta_sub_project_entity.sub_meta_pro_approval_settings_role_rel

        current_rel_info_ids = set((rel.approval_role_id.id, rel.employee_id.id) for rel in current_rel_entities)
        target_rel_info_ids = set((approval_role_info['approval_role_id'], employee_info['employee_id'])
                                     for approval_role_info in meta_sub_project_info['approval_role_infos']
                                     for employee_info in approval_role_info['employee_infos'])


        todoremove_ids = current_rel_info_ids - target_rel_info_ids
        todoadd_ids = target_rel_info_ids - current_rel_info_ids

        # tuple_id ( approval_role_id, employee_id)

        res = current_rel_entities.filtered(lambda rel: (rel.approval_role_id.id, rel.employee_id.id) in todoremove_ids)
        res.unlink()

        # for tuple_id in todoremove_ids:
        #
        #     for rel_entity in current_rel_entities:
        #         if rel_entity.approval_role_id.id == tuple_id[0] and rel_entity.employee_id.id == tuple_id[1]:
        #             rel_entity.unlink()
        #             break


        for tuple_id in todoadd_ids:
            current_rel_entities.create({
                'meta_sub_project_id': meta_sub_project_entity.id,
                'approval_role_id': tuple_id[0],
                'employee_id': tuple_id[1],
            })

    # 复制已有的配置,所有的主工程下面的子工程

    def rpc_copy_all_permission_configuration(self):
        project_entities = self.search([])
        res = []
        for project_entity in project_entities:
            for meta_pro_entity in project_entity.meta_sub_project_ids:
                round_financing_and_Foundation_entity = meta_pro_entity.round_financing_and_Foundation_ids[0]
                round_financing_name = round_financing_and_Foundation_entity.round_financing_id.name if round_financing_and_Foundation_entity.round_financing_id \
                    else u'暂无轮次'

                foundation_name = round_financing_and_Foundation_entity.foundation_id.name if round_financing_and_Foundation_entity.foundation_id \
                    else u'暂无基金'

                sub_project_entity = meta_pro_entity.sub_project_ids

                sub_project_name = sub_project_entity.name if sub_project_entity else u'暂无子工程'
                res.append({
                    'meta_sub_project_id': meta_pro_entity.id,
                    'sub_project_name': sub_project_name,
                    'round_financing_name': round_financing_name,
                    'foundation_name': foundation_name,
                })

        return res


    def rpc_copy_permission_configuration(self, **kwargs):

        current_meta_sub_pro_id = kwargs['current_meta_sub_pro_id']
        copy_meta_sub_pro_id = kwargs['copy_meta_sub_pro_id']


        # current_meta_sub_pro_entity = self.meta_sub_project_ids.browse(current_meta_sub_pro_id)
        copy_meta_sub_pro_entity = self.meta_sub_project_ids.browse(copy_meta_sub_pro_id)

        # return copy_meta_sub_pro_entity.copy_data()

        copy_rel_entities = copy_meta_sub_pro_entity.sub_meta_pro_approval_settings_role_rel

        res = []
        for c_rel_entity in copy_rel_entities:
            t = c_rel_entity.create({
                'meta_sub_project_id': current_meta_sub_pro_id,
                'approval_role_id':c_rel_entity.approval_role_id.id,

                'employee_id': c_rel_entity.employee_id.id,
            })

            res.append(t)

            # t = c_rel_entity.copy_data({
            #     'meta_sub_project_id': current_meta_sub_pro_id,
            #     'approval_role_id': c_rel_entity.approval_role_id.id,
            #     'employee_id': c_rel_entity.employee_id.id,
            # })
            #
            #
            # res.append(t[0])





        result = self.rpc_get_permission_configuration()
        # 前端数据的需要的临时的操作!!!
        for i in res:
            i.unlink()

        return result


    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        print(u'该方法应该是可以回执行的!!!')
        # 该方法中有四个状态需要考虑
        # (1, 1) --> 投前流程 (1, 2) --> 投前审批
        # (2, 1) --> 投后流程 (2, 2) --> 投后审批
        # (3, 1) --> 全局搜索,只读模式
        prev_or_post_investment = self._context.get('prev_or_post_investment')

        prev_or_post_investment = tuple(prev_or_post_investment) if prev_or_post_investment else ()

        entities = super(Cowin_project, self).search(args, offset, limit, order, count)
        # return entities

        if self.env.user.id == SUPERUSER_ID:
            return entities

        if type(self.env[self._name]).get_created():
            type(self.env[self._name]).update_created(False)
            return entities

        to_filter_projects = set()

        # return self.env[self._name]

        if prev_or_post_investment is None:
            return entities

        # 投前流程
        elif prev_or_post_investment == (1, 1):

            # # 接下来需要考虑属于每个工程的虚拟角色问题
            for entity in entities:
                # 发起人所对应的角色
                # operation_role_entitis = set()
                # for stage_entity in entity.process_id.stage_ids:
                #     if stage_entity.prev_or_post_investment:
                #         # 投前
                #         for tache_entity in stage_entity.tache_ids:
                #             if tache_entity.model_id.model_name == self._name:
                #                 continue
                #             # 把提交角色放入提取出来
                #             operation_role_entitis\
                #                 .add(tache_entity.approval_flow_settings_ids.approval_flow_setting_node_ids[1].operation_role_id)
                #

                # 获得所有的发起人的角色之后,还需要依据元子工程过滤中该主工所有三张表之间依赖的实体
                # 找到该主工程中,发起人所关联的employee
                target_employ_entities = set()


                for meta_sub_pro_entity in entity.meta_sub_project_ids:
                    restrict_rels = meta_sub_pro_entity.sub_meta_pro_approval_settings_role_rel
                    # for role in operation_role_entitis:
                    #     rel_entities = restrict_rels & role.sub_meta_pro_approval_settings_role_rel


                        # for rel_entity in rel_entities:
                        #     target_employ_entities.add(rel_entity.employee_id)
                    for rel in restrict_rels:
                        target_employ_entities.add(rel.employee_id)



                # 当前用户所对应的employee
                current_employee_entities = set(self.env.user.employee_ids)
                employee_e = current_employee_entities & target_employ_entities


                if employee_e:
                    to_filter_projects.add(entity)
                elif entity.create_uid == self.env.user:
                    to_filter_projects.add(entity)
                else:
                    pass







        # 投前审批
        elif prev_or_post_investment == (1, 2):
            # # 接下来需要考虑属于每个工程的虚拟角色问题
            for entity in entities:
                # if not entity.prev_or_post_investment:
                #     continue
                # 发起人所对应的角色
                operation_role_entitis = set()
                for stage_entity in entity.process_id.stage_ids:
                    if stage_entity.prev_or_post_investment:
                        # 投前
                        for tache_entity in stage_entity.tache_ids:
                            if tache_entity.model_id.model_name == self._name:
                                continue
                            # 把提交角色放入提取出来

                            approval_flow_settings_entity = tache_entity.approval_flow_settings_ids
                            approval_node_entities = list(approval_flow_settings_entity.approval_flow_setting_node_ids)
                            # 大于2的意义在于这个除了提交节点和结束节点之外,还有审核节点
                            if len(approval_node_entities) > 2:
                                # 这个sub_approval_flow_settings_ids 代表的意思在于每个主工程中的元子工程都会有子审批流
                                for sub_approval_entity in approval_flow_settings_entity.sub_approval_flow_settings_ids:
                                    # 数据库的取巧操作,前两个分别是提交结束,提交,后面的都是审核节点,并且是以此顺序存储
                                    if sub_approval_entity.status == 2 :
                                        if not sub_approval_entity.current_approval_flow_node_id:
                                            # 还未发起
                                            continue
                                        node_index = approval_node_entities.index(sub_approval_entity.current_approval_flow_node_id)


                                        operation_role_entitis |= set(node.operation_role_id for node in approval_flow_settings_entity.approval_flow_setting_node_ids[2:node_index+1])

                # 获得所有的发起人的角色之后,还需要依据元子工程过滤中该主工所有三张表之间依赖的实体
                # 找到该主工程中,发起人所关联的employee
                target_employ_entities = set()

                for meta_sub_pro_entity in entity.meta_sub_project_ids:
                    restrict_rels = meta_sub_pro_entity.sub_meta_pro_approval_settings_role_rel
                    for role in operation_role_entitis:
                        rel_entities = restrict_rels & role.sub_meta_pro_approval_settings_role_rel

                        for rel_entity in rel_entities:
                            target_employ_entities.add(rel_entity.employee_id)

                # 当前用户所对应的employee
                current_employee_entities = set(self.env.user.employee_ids)
                employee_e = current_employee_entities & target_employ_entities

                if employee_e:
                    to_filter_projects.add(entity)


        # 投后流程
        elif prev_or_post_investment == (2, 1):

            # # 接下来需要考虑属于每个工程的虚拟角色问题
            for entity in entities:
                # 如果还是投前状态,那么需要过滤过去
                # 如果是投后状态,那么这个值就是false
                if entity.prev_or_post_investment:
                    continue
                # 发起人所对应的角色
                # operation_role_entitis = set()
                # for stage_entity in entity.process_id.stage_ids:
                #     if not stage_entity.prev_or_post_investment:
                #         # 投前
                #         for tache_entity in stage_entity.tache_ids:
                #             if tache_entity.model_id.model_name == self._name:
                #                 continue
                #             # 把提交角色放入提取出来
                #             operation_role_entitis \
                #                 .add(tache_entity.approval_flow_settings_ids.approval_flow_setting_node_ids[
                #                          1].operation_role_id)

                # 获得所有的发起人的角色之后,还需要依据元子工程过滤中该主工所有三张表之间依赖的实体
                # 找到该主工程中,发起人所关联的employee
                target_employ_entities = set()

                for meta_sub_pro_entity in entity.meta_sub_project_ids:
                    restrict_rels = meta_sub_pro_entity.sub_meta_pro_approval_settings_role_rel
                    # for role in operation_role_entitis:
                    #     rel_entities = restrict_rels & role.sub_meta_pro_approval_settings_role_rel

                        # for rel_entity in rel_entities:
                        #     target_employ_entities.add(rel_entity.employee_id)
                    for rel in restrict_rels:
                        target_employ_entities.add(rel.employee_id)


                # 当前用户所对应的employee
                current_employee_entities = set(self.env.user.employee_ids)
                employee_e = current_employee_entities & target_employ_entities

                if employee_e:
                    to_filter_projects.add(entity)
                elif entity.create_uid == self.env.user:
                    to_filter_projects.add(entity)
                else:
                    pass

                # # 当前工程所有元子工程操作角色
                #
                # approval_role_entities = set()
                # for meta_sub_pro_entity in entity.meta_sub_project_ids:
                #     # 多个这样的关系
                #     for rel_entity in meta_sub_pro_entity.sub_meta_pro_approval_settings_role_rel:
                #         approval_role_entities.add(rel_entity.approval_role_id)
                #
                # # 注:当前用户所对应的虚拟角色可能跨越多个主工程
                # current_approle_entities = set(rel_entity.approval_role_id for rel_entity in
                #                                self.env.user.employee_ids.sub_meta_pro_approval_settings_role_rel)
                #
                # if approval_role_entities & current_approle_entities & operation_role_entitis:
                #     to_filter_projects.add(entity)


        # 投后审批
        elif prev_or_post_investment == (2, 2):

            # # 接下来需要考虑属于每个工程的虚拟角色问题
            for entity in entities:

                # 如果还是投前状态,那么需要过滤过去
                # 如果是投后状态,那么这个值就是false
                if entity.prev_or_post_investment:
                    continue

                # 发起人所对应的角色
                operation_role_entitis = set()
                for stage_entity in entity.process_id.stage_ids:
                    if not stage_entity.prev_or_post_investment:
                        # 投前
                        for tache_entity in stage_entity.tache_ids:
                            if tache_entity.model_id.model_name == self._name:
                                continue
                            # 把提交角色放入提取出来

                            approval_flow_settings_entity = tache_entity.approval_flow_settings_ids
                            approval_node_entities = list(approval_flow_settings_entity.approval_flow_setting_node_ids)
                            # 大于2的意义在于这个除了提交节点和结束节点之外,还有审核节点
                            if len(approval_node_entities) > 2:
                                # 这个sub_approval_flow_settings_ids 代表的意思在于每个主工程中的元子工程都会有子审批流
                                for sub_approval_entity in approval_flow_settings_entity.sub_approval_flow_settings_ids:
                                    # 数据库的取巧操作,前两个分别是提交结束,提交,后面的都是审核节点,并且是以此顺序存储
                                    if sub_approval_entity.status == 2 :
                                        if not sub_approval_entity.current_approval_flow_node_id:
                                            # 还未发起
                                            continue
                                        node_index = approval_node_entities.index(sub_approval_entity.current_approval_flow_node_id)


                                        operation_role_entitis |= set(node.operation_role_id for node in approval_flow_settings_entity.approval_flow_setting_node_ids[2:node_index+1])

                # 获得所有的发起人的角色之后,还需要依据元子工程过滤中该主工所有三张表之间依赖的实体
                # 找到该主工程中,发起人所关联的employee
                target_employ_entities = set()

                for meta_sub_pro_entity in entity.meta_sub_project_ids:
                    restrict_rels = meta_sub_pro_entity.sub_meta_pro_approval_settings_role_rel
                    for role in operation_role_entitis:
                        rel_entities = restrict_rels & role.sub_meta_pro_approval_settings_role_rel

                        for rel_entity in rel_entities:
                            target_employ_entities.add(rel_entity.employee_id)

                # 当前用户所对应的employee
                current_employee_entities = set(self.env.user.employee_ids)
                employee_e = current_employee_entities & target_employ_entities

                if employee_e:
                    to_filter_projects.add(entity)

                # # 注:当前用户所对应的虚拟角色可能跨越多个主工程
                # current_approle_entities = set(rel_entity.approval_role_id for rel_entity in
                #                                self.env.user.employee_ids[0].sub_meta_pro_approval_settings_role_rel)
                #
                # # if approval_role_entities & current_approle_entities & operation_role_entitis:
                # if current_approle_entities & operation_role_entitis:
                #     to_filter_projects.add(entity)

        else:
            return entities

        tem = self.env[self._name]



        res = reduce(lambda x, y: x | y, to_filter_projects, tem)

        return res




    def rpc_get_operation_record(self):

        # selection_info = [
        #     {'operation': u'提交'},]
        #     {'operation': u'提交'},]
        #     {'operation': u'提交'},]
        #     {'operation': u'提交'},]
        #     {'operation': u'提交'},]
        ids = []
        model_name = u''
        for meta_sub_project_entity in self.meta_sub_project_ids:
            # 子审批流程实体
            model_name = meta_sub_project_entity.sub_approval_flow_settings_ids._name
            for entity in meta_sub_project_entity.sub_approval_flow_settings_ids:
                ids.append(entity.id)


        res_entity = self.env['mail.message'].search([('res_id', 'in', ids), ('model', '=', model_name)])

        res_entity = res_entity.read(fields=['body'])
        for e in res_entity:
            # 删除<p>  </p> 标签
            t = html2plaintext(e['body'])
            try:
                e['body'] = json.loads(t)
            except:
                e['body'] = None


        return {'operation_records': filter(lambda x: x['body'], res_entity)}


    @api.multi
    def unlink(self):

        for record in self:
            # 因为有通信模块的操作,所以需要指定在主工程中做删除

            record.process_id.unlink()
            super(Cowin_project, record).unlink()

        return True
        # return self.process_id.unlink()
        # for record  in self:
        #     record.unlink()


    # 查看按钮的显示类型
    def rpc_approval_view_action_action(self, **kwargs):
        tache_info = kwargs['tache_info']

        sub_tache_id = tache_info['sub_tache_id']
        meta_sub_project_id = tache_info['meta_sub_project_id']

        meta_sub_project_entity = self.meta_sub_project_ids.browse(meta_sub_project_id)
        sub_tache_entity = meta_sub_project_entity.sub_tache_ids.browse(sub_tache_id)

        res_id = sub_tache_entity.res_id

        model_name = sub_tache_entity.tache_id.model_id.model_name

        return self.env[model_name].browse(res_id).approval_view_action_action()


    # 每次发起之前,需要请求之前的数据,业务需求的原因,需要把之前老的数据填充到新建的实体之中!!!
    def rpc_load_and_return_action(self, **kwargs):

        tache_info = kwargs['tache_info']


        sub_tache_id = tache_info['sub_tache_id']
        meta_sub_project_id = tache_info['meta_sub_project_id']

        meta_sub_project_entity = self.meta_sub_project_ids.browse(meta_sub_project_id)
        sub_tache_entity = meta_sub_project_entity.sub_tache_ids.browse(sub_tache_id)



        res_id = sub_tache_entity.res_id

        model_name = sub_tache_entity.tache_id.model_id.model_name

        return self.env[model_name].browse(res_id).load_and_return_action(**kwargs)




    # 审核按钮的操作!!!
    def rpc_approval_launch_action(self, **kwargs):
        tache_info = kwargs['tache_info']

        sub_tache_id = tache_info['sub_tache_id']
        meta_sub_project_id = tache_info['meta_sub_project_id']

        meta_sub_project_entity = self.meta_sub_project_ids.browse(meta_sub_project_id)
        sub_tache_entity = meta_sub_project_entity.sub_tache_ids.browse(sub_tache_id)

        res_id = sub_tache_entity.res_id

        model_name = sub_tache_entity.tache_id.model_id.model_name

        return self.env[model_name].browse(res_id).approval_launch_action()


    # def rpc_test_cowin_project(self):
    #
    #     return {
    #         'name': self.name,
    #         'type': 'ir.actions.act_window',
    #         'res_model': self._name,
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'view_id': False,
    #         'res_id': self.id,
    #         'target': 'new',
    #         'context': {'default_name': 'kkkkk'},
    #     }



    # 获得联系人的信息!!!
    def rpc_get_contract_info(self):

        contract_infos = []

        for meta_sub_project_entity in self.meta_sub_project_ids:

            sub_project_entity = meta_sub_project_entity.sub_project_ids

            if not sub_project_entity:
                continue

            sub_project_entity = sub_project_entity[0]


            related_sub_project = u'%s/%s/%s' % (
                sub_project_entity.name,
                sub_project_entity.meta_sub_project_id.round_financing_and_Foundation_ids[0].round_financing_id.name,
                sub_project_entity.meta_sub_project_id.round_financing_and_Foundation_ids[0].foundation_id.name)

            contract_info = {
                'company_name': self.name,
                'customer_position': '',
                'contract_person': sub_project_entity.contract_person,
                'contract_phone': sub_project_entity.contract_phone,
                'contract_email': sub_project_entity.contract_email,
                'related_sub_project': related_sub_project
            }

            contract_infos.append(contract_info)


            call_up_records = self.env['cowin_project.sub_call_up_record'].sudo().search([('subproject_id', '=', sub_project_entity.id)])

            for call_up_reco in call_up_records:
                contract_infos.append({
                    'company_name': call_up_reco.customer_company_name,
                    'customer_position': call_up_reco.customer_position,
                    'contract_person': call_up_reco.customer_name,
                    'contract_phone': call_up_reco.customer_contract,
                    'contract_email': call_up_reco.customer_email,
                    'related_sub_project': related_sub_project,
                })



        return {'contract_infos': contract_infos}







    # 新增 创建 基金轮次实体接口
    def rpc_new_found_round_entity(self, **kwargs):

        data_version = kwargs.get('data_version')
        name = 'cowin_project.cowin_subproject'

        if data_version != self.data_version:
            raise UserError(u'新的子工程实体已经被其他用户添加,请刷新界面!')

        # 数据版本增加
        self.data_version += 1


        # res = {'rpc_new_found_round_entity': True}

        res = {
            'rec_new_found_round_info': {
                'project_id': self.id,
            }
        }


        # self.whether_new_meta_sub_project_or_not = False

        return {
            'name': u'项目立项',
            'type': 'ir.actions.act_window',
            'res_model': name,
            'views': [[False, 'form']],
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'target': 'current',
            'context': res,
        }



    # 由于 在compute字段中,数据是先返回之前的数据,然后、去保存修改之后的数据,所以需要做两次数据的访问,这是业务的需求!!!
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):

        super(Cowin_project, self).search_read(domain, fields, offset, limit, order)
        res = super(Cowin_project, self).search_read(domain, fields, offset, limit, order)

        return res

        # return super(Cowin_project, self).unlink()


# class Project_roles(models.Model):
#     _name = 'cowin_project.project_approval_role'
#     '''
#         工程审批角色的: 目的在于方便的操作虚拟角色操作
#     '''
#
#
#     project_id = fields.Many2one('cowin_project.cowin_project', string=u'主工程', ondelete="cascade")
#
#     status = fields.Selection([(1, u'投前发起角色'), (2, u'投前审批角色'), (3, u'投后发起角色'), (4, u'投后审批角色')], string=u'投前投后阶段')
#
#     approval_role_ids = fields.Many2many('cowin_common.approval_role', 'cowin_approval_role_cowin_project_rel', string=u'虚拟角色')

    # 获得详情的信息!!!
    def rpc_get_detail_info(self):
        #is_final_meeting_resolution
        detail_infos = []
        project_details = self.env['cowin.project.detail'].sudo().search([('project_id', '=', self.id)])

        for project_detail in project_details:
            project_detail = {
                'round_financing_id': project_detail.round_financing_id.name,
                'the_amount_of_financing': project_detail.the_amount_of_financing,
                'ownership_interest': project_detail.ownership_interest,
                'the_amount_of_investment': project_detail.the_amount_of_investment,
                'foundation': project_detail.foundation,
            }

            detail_infos.append(project_detail)

        return {'detail_infos': detail_infos}