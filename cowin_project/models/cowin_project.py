# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.modules.module import get_module_resource
from odoo import tools
from odoo.exceptions import UserError
from odoo import SUPERUSER_ID


class Cowin_project(models.Model):
    _name = 'cowin_project.cowin_project'

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

    name = fields.Char(string=u"项目名称", required=True)

    project_number = fields.Char(string=u'项目编号',
                                 defualt=lambda self: self.env['ir.sequence'].next_by_code('cowin_project.order'))
    project_source = fields.Selection([(1, u'朋友介绍'), (2, u'企业自荐')],
                              string=u'项目来源', required=True)
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

    attachment_ids = fields.Many2many('ir.attachment', string=u"附件")


    attachment_note = fields.Char(string=u'附件说明')

    # @api.model
    def _iscurrentUser_and_Admin(self):
        '''

        :return:
        '''

        # 检测当前的用户是否是管理员
        if self.env.user.id == SUPERUSER_ID:
            return True


        # 每个主工程所有的元子工程信息
        for meta_sub_pro_entity in self.meta_sub_project_ids:

            # 每个元子工程的子审批流信息
            for sub_approval_flow_entity in meta_sub_pro_entity.sub_approval_flow_settings_ids:

                # 每个子审批流所对应的当前的操作角色
                current_role_entity = sub_approval_flow_entity.current_approval_flow_node_id.operation_role_id
                # 当前用户所关联的操作角色
                all_role_entities = self.env.user.employee_ids.approval_role_ids

                if current_role_entity in all_role_entities:
                    return True

        return False

    iscurrentUser_and_Admin = fields.Boolean(string=u'当前的用户是否有权限审批', default=_iscurrentUser_and_Admin)



    # 考虑到设计上的规则性,每个工程的创建需要做很多的事情
    @api.model
    def create(self, vals):

        # 1, 创建工程配置实例
        process = None
        if not vals.get('project_number'):
            vals['project_number'] = self.env['ir.sequence'].next_by_code('cowin_project.order')

        if not vals.get('process_id'):
            meta_setting_entity = self.env['cowin_settings.process'].search([('category', '=', 'init_preinvestment')])

            # 每次创建的实例 都要从数据
            # process = self.env['cowin_project.process'].create_process_info(meta_setting_entity.copy_custom(),
            #                                                                 meta_setting_entity.id)


            # 注意,这个self只是代表着一个空的project实体,方便以后的使用!!!
            process = self.process_id.create_process_info(meta_setting_entity.copy_custom())

            vals['process_id'] = process.id


        project = super(Cowin_project, self).create(vals)


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
        })


        # self.env['cowin_project.round_financing_and_foundation'].create({
        #     'meta_sub_project_id': meta_sub_project.id,
        #     # 很显然,这种情况下是只能是为空的,因为是第一次的操作!!!
        #     'sub_invest_decision_committee_res_id': None,
        # })


        # 1-2 默认创建该元子工程实例一个基金轮次实例
        meta_sub_project.round_financing_and_Foundation_ids.create({
            'meta_sub_project_id': meta_sub_project.id,
            # 很显然,这种情况下是只能是为空的,因为是第一次的操作!!!
            'sub_invest_decision_committee_res_id': None,
        })

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
    def process_settings2(self, meta_sub_project_id):
        '''

        :param meta_sub_project_id: 子工程实例id
        :return:
        '''

        # 1 获取原始的配置信息
        process_info = self.process_id.get_info()


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





        # 3 元子工程信息中存在的字环节与原始环节进行合并配置

        sub_tache_entities = meta_sub_project_entity.get_sub_taches()
        tache_infos = [tache_info for stage in process_info['stage_ids']
                  for tache_info in stage['tache_ids']]

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
        for stage in process_info['stage_ids']:
            res = True
            for tache_info in stage['tache_ids']:
                if tache_info['model_name'] == self._name:
                    res = False

            if res:
                stages.append(stage)


        for stage in stages:
            # 从新渲染装配
            stage['tache_ids'] = []

            for sub_tache_entity in sub_tache_entities:
                if sub_tache_entity.tache_id.stage_id.id == stage['id']:
                    tache_info = {}
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
                    tache_info['once_or_more'] = sub_tache_entity.tache_id.once_or_more
                    tache_info['view_or_launch'] = sub_tache_entity.view_or_launch
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

                    # True 代表着审核状态
                    approval_view_or_launch = None
                    if status == 1:
                        # 未开始审核
                        info = u'暂无'
                    elif status == 2:
                        # 审核中...
                        # 找出当前的审核人


                        # 考虑到可能改子环节还没有开始发起,所以也是直接回到 '暂无状态'
                        if not sub_tache_entity.view_or_launch:
                            info = u'暂无'
                        else:
                            # 当前的虚拟角色名
                            name = target_sub_approval_flow_entity.current_approval_flow_node_id.operation_role_id.name

                            current_approval_flow_entity = target_sub_approval_flow_entity.current_approval_flow_node_id.operation_role_id

                            # 当前虚拟角色所属的员工
                            employee_ids = current_approval_flow_entity.employee_ids

                            # 需要考虑到是不同的元子工程来配置角色,获得到时虚拟角色和员工之间的M 2 M之间的关系
                            approval_role_and_employee_ids = meta_sub_project_entity.approval_role_and_employee_ids

                            # 当前员工所对应的角色
                            approval_role_ids = self.env.user.employee_ids.approval_role_ids

                            # current_user_approval_flow_ids = self.env.user.employee_ids.approval_role_ids

                            info = u'待%s审核' % name

                            # 接下来要考虑当前用户是否属于某一个虚拟角色
                            # if current_approval_flow_entity in current_user_approval_flow_ids:
                            if approval_role_and_employee_ids & employee_ids & approval_role_ids:
                                # 很显然当前用户可以审批
                                approval_view_or_launch = True
                            else:
                                # 很显然不需要去审批,因为没有这个
                                approval_view_or_launch = False

                            if self.env.user.id == SUPERUSER_ID:
                                approval_view_or_launch = True

                    elif status == 3:
                        # 暂缓
                        info = u'暂缓'
                    elif status == 4:
                        # 同意
                        info = u'同意'
                        approval_view_or_launch = False
                    elif status == 5:
                        # 拒绝
                        info = u'拒绝'
                        approval_view_or_launch = False
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



                    stage['tache_ids'].append(tache_info)

                    break


        return process_info['stage_ids']




    # 获得每个project的详细信息
    def _get_info(self, **kwargs):
        tmp = kwargs.get("meta_project_id")
        meta_project_id = 0 if not tmp else int(tmp)

        return {'id': self.id,
                'name': self.name,
                'process_id': self.process_id.id,
                'image': self.image,
                'project_number': self.project_number,
                'project_source': self.project_source,
                'project_source_note': self.project_source_note,
                # 'invest_manager': self.invest_manager,
                'round_financing': self.round_financing.name,
                'round_money': self.round_money,
                'project_company_profile': self.project_company_profile,
                'project_appraisal': self.project_appraisal,
                'project_note': self.project_note,
                # 'industry': self.industry,
                'stage': self.stage,
                'production': self.production,
                'registered_address': self.registered_address,
                'peration_place': self.peration_place,
                'founding_time': self.founding_time,
                'contract_person': self.contract_person,
                'contract_phone': self.contract_phone,
                'contract_email': self.contract_email,
                'attachment_note': self.attachment_note,
                'investment_funds': self.get_investment_funds(),
                'process': self.process_settings2(meta_project_id),
                'permission_configuration': self.rpc_get_permission_configuration(),
                }


    #
    # def get_all_investment_funds(self):
    #     return [funds for funds in self.investment_funds]

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
        return self._get_info(**kwargs)


    # 新增子环节
    def new_sub_tache(self, **kwargs):

        meta_sub_project_id = kwargs['meta_sub_project_id']
        current_sub_tache_id = kwargs['sub_tache_id']

        meta_sub_project_entity = self.meta_sub_project_ids.browse(meta_sub_project_id)
        sub_tache_entity = meta_sub_project_entity.sub_tache_ids.browse(current_sub_tache_id)
        current_tache_entity = sub_tache_entity.tache_id


        # 获取当前子环节所有的兄弟环节
        brother_sub_tache_entities = meta_sub_project_entity.sub_tache_ids & current_tache_entity.tache_status_ids

        brother_sub_tache_entities = brother_sub_tache_entities.sorted('index')

        is_last = True
        for sub_tache_e in meta_sub_project_entity.sub_tache_ids:
            if sub_tache_e.parent_id == sub_tache_entity:
                # 如果数据已经解锁的话,向前端报错,不能有这样的情况产生
                if sub_tache_e.is_unlocked:
                    raise UserError(u'被依赖的环节已经接解锁!!!')
                # index = brother_sub_tache_entities[-1].index + 1



        for sub_tache_e in meta_sub_project_entity.sub_tache_ids:

            if sub_tache_e.parent_id == brother_sub_tache_entities[-1]:
                is_last = False
                # 如果数据已经解锁的话,向前端报错,不能有这样的情况产生
                # if sub_tache_e.is_unlocked:
                #     raise UserError(u'依赖的环节已经接解锁!!!')
                index = brother_sub_tache_entities[-1].index + 1

                # 新增子环节
                new_sub_tache_entity = brother_sub_tache_entities.create({
                    'name': brother_sub_tache_entities[0].name + ' ' + str(index),
                    'meta_sub_project_id': sub_tache_entity.meta_sub_project_id.id,
                    'tache_id': sub_tache_entity.tache_id.id,
                    'parent_id': brother_sub_tache_entities[-1].id,
                    'index': index,
                })

                sub_tache_e.write({
                    'parent_id': new_sub_tache_entity.id,
                })

                # 还需要新增子审批实体

                new_sub_tache_entity.sub_pro_approval_flow_settings_ids.create({
                    'sub_project_tache_id': new_sub_tache_entity.id,
                    'meta_sub_project_id': meta_sub_project_entity.id,
                    # 理论上主环节中只有一份主审批流实体
                    'approval_flow_settings_id': new_sub_tache_entity.tache_id.approval_flow_settings_ids.id,
                    # 默认就指向第一个位置!!!
                    'current_approval_flow_node_id': new_sub_tache_entity.tache_id.approval_flow_settings_ids.
                            approval_flow_setting_node_ids.sorted('order')[0].id,
                })






                # 每次都需要调用这个方法
                meta_sub_project_entity.sub_tache_ids.set_depency_order_by_sub_tache()

                break


        if is_last:
            index = brother_sub_tache_entities[-1].index + 1
            brother_sub_tache_entities.create({
                'name': brother_sub_tache_entities[-1].name + ' ' + str(index),
                'meta_sub_project_id': sub_tache_entity.meta_sub_project_id.id,
                'tache_id': sub_tache_entity.tache_id.id,
                'parent_id': sub_tache_entity.id,
                'index': index,
            })

            meta_sub_project_entity.sub_tache_ids.set_depency_order_by_sub_tache()


        return self._get_info()













    # 派生继承之后的方法=
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):

        # 在这个地方做拦截,拦截action在后台取数据,以及要绑定到的当前的用户是否为当前审批节点需要的用户!!!
        all_projects = self.search([])
        for pro_entity in all_projects:
            pro_entity.write({
                'iscurrentUser_and_Admin': True if self._iscurrentUser_and_Admin() else False
            })

        return super(Cowin_project, self).search_read(domain, fields, offset, limit, order)



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


        approval_flow_settings_record_info = kwargs.get('approval_flow_settings_record')

        # 理论上只会有一个员工  审批人
        approval_flow_settings_record_info['approval_person_id'] = self.env.user.employee_ids.id

        # 审批角色
        approval_flow_settings_record_info['approval_role_id'] = sub_approval_flow_settings_entity.current_approval_flow_node_id.operation_role_id.id

        # 更新审批节点 拿到当前的子环节

        sub_approval_flow_settings_entity.save_approval_flow_info(approval_flow_settings_record_info)

        # 触发下一个子环节
        current_sub_tache_entity = meta_sub_project_entity.sub_tache_ids.browse(tache_info['sub_tache_id'])

        if sub_approval_flow_settings_entity.is_success():
            for sub_tache_entity in meta_sub_project_entity.get_sub_taches():
                if sub_tache_entity.parent_id == current_sub_tache_entity:
                    sub_tache_entity.write({
                        'is_unlocked': True,
                        # 'status': 2,
                    })


                    # 在触发下一个子环节过程中,还需要触发下一个子环节所对应的子审批节点信息

                    sub_approval_flow_settings_entity_next = sub_tache_entity.sub_pro_approval_flow_settings_ids

                    sub_approval_flow_settings_entity_next.write({
                        'status': 2,
                    })

                    break


        return self._get_info(meta_project_id=meta_sub_project_id)




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

            approval_role_repr = meta_sub_pro_entity.approval_role_and_employee_ids[0] if meta_sub_pro_entity.approval_role_and_employee_ids else meta_sub_pro_entity.approval_role_and_employee_ids
            approval_role_ids = approval_role_repr.approval_role_id.search([])

            employee_repr = meta_sub_pro_entity.approval_role_and_employee_ids[0] if meta_sub_pro_entity.approval_role_and_employee_ids else meta_sub_pro_entity.approval_role_and_employee_ids
            employee_ids = employee_repr.employee_id.search([])

            default_is_full = True

            for approval_role_entity in approval_role_ids:
                tmp2 = {}
                tmp2['approval_role_id'] = approval_role_entity.id
                tmp2['approval_role_name'] = approval_role_entity.name

                tmp2['employee_infos'] = [{'employee_id': approval_employee_rel.employee_id.id, 'name': approval_employee_rel.employee_id.name_related}
                    for approval_employee_rel in meta_sub_pro_entity.approval_role_and_employee_ids if approval_employee_rel.approval_role_id == approval_role_entity]


                if not tmp2['employee_infos']:
                    default_is_full = False


                tmp['approval_role_infos'].append(tmp2)

            tmp['default_is_full'] = default_is_full

            default_is_full &= tmp['default_is_full']

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

        for meta_sub_project_entity in self.meta_sub_project_ids:

            for meta_sub_project_info in meta_sub_project_infos:
                if meta_sub_project_info['meta_sub_pro_id'] == meta_sub_project_entity.id:
                    self._save_permission_configuration(meta_sub_project_entity, meta_sub_project_info)
                    break

        return self.rpc_get_permission_configuration()



    def _save_permission_configuration(self, meta_sub_project_entity, meta_sub_project_info):



        current_rel_entities = meta_sub_project_entity.approval_role_and_employee_ids

        current_rel_info_ids = set((rel.approval_role_id.id, rel.employee_id.id) for rel in current_rel_entities)
        target_rel_info_ids = set((approval_role_info['approval_role_id'], employee_info['employee_id'])
                                     for approval_role_info in meta_sub_project_info['approval_role_infos']
                                     for employee_info in approval_role_info['employee_infos'])

        todoremove_ids = current_rel_info_ids - target_rel_info_ids
        todoadd_ids = target_rel_info_ids - current_rel_info_ids

        for tuple_id in todoremove_ids:

            for rel_entity in current_rel_entities:
                if rel_entity.approval_role_id.id == tuple_id[0] and rel_entity.employee_id.id == tuple_id[1]:
                    rel_entity.unlink()
                    break


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

        copy_rel_entities = copy_meta_sub_pro_entity.approval_role_and_employee_ids

        for c_rel_entity in copy_rel_entities:
            c_rel_entity.create({
                'meta_sub_project_id': current_meta_sub_pro_id,
                'approval_role_id':c_rel_entity.approval_role_id.id,
                'employee_id': c_rel_entity.employee_id.id,
            })





        return self.rpc_get_permission_configuration()




