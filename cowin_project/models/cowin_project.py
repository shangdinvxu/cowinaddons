# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.modules.module import get_module_resource
from odoo import tools
import copy

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
            process = self.env['cowin_project.process'].create_process_info(meta_setting_entity.copy_custom(),
                                                                            meta_setting_entity.id)

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
                    'is_unlocked': True,
                    'view_or_launch': True,
                    'once_or_more': False,
                })

                break


        # 1 添加审批流配置信息
        for tache in process.get_all_tache_entities():
            approval_flow_settings_entity = tache.approval_flow_settings_ids






        # 2-1 默认创建 元子工程实例

        meta_sub_project = self.env['cowin_project.meat_sub_project'].create({
            'project_id': project.id,
        })

        # 2-2 默认创建该元子工程实例一个基金轮次实例
        r_f_a_f = self.env['cowin_project.round_financing_and_foundation'].create({
            'meta_sub_project_id': meta_sub_project.id,
            'sub_invest_decision_committee_res_id': 0,
        })

        # # 2-3 默认构建一条轮次基金实体
        # meta_sub_project.write({
        #     'round_financing_and_Foundation': r_f_a_f.id,
        # })

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
        process = self.process_id.get_info()


        # 2 获取指定的一个元子工程信息
        meta_sub_project_entity = None
        # 代表着第一次默认选择第一个来显示,当然,如果存在的情况下
        # 返回给客户的时候页面需要默认显示的一条轮次基金数据
        if not meta_sub_project_id:
            '''意思在于如果主工程子工程数据,那就显示子工程数据,否则就返回为空'''
            meta_sub_project_entity = self.meta_sub_project_ids

            # 第一条数据存在
            if meta_sub_project_entity:
                meta_sub_project_entity = meta_sub_project_entity[0]

        else:
            for meta_sub_pro in self.meta_sub_project_ids:
                if meta_sub_pro.id == meta_sub_project_id:
                    meta_sub_project_entity = meta_sub_pro



        # 3 元子工程信息中存在的字环节与原始环节进行合并配置


        sub_taches = meta_sub_project_entity.get_sub_taches()

        taches = [tache for stage in process['stage_ids']
                  for tache in stage['tache_ids']]

        for sub_tache in sub_taches:
            for tache in taches:
                if tache['id'] == sub_tache.tache_id.id:
                    tache['sub_tache_id'] = sub_tache.id
                    tache['res_id'] = sub_tache.res_id



                    #  1  <--------------- 需要传递的上下文信息,共享的基金轮次实体
                    tache['round_financing_and_foundation'] = {}

                    tache['round_financing_and_foundation']['round_financing_and_foundation_id'] = meta_sub_project_entity.\
                                                         round_financing_and_Foundation_ids[0].id

                    tache['round_financing_and_foundation']['foundation_id'] = meta_sub_project_entity.\
                                                         round_financing_and_Foundation_ids[0].foundation_id.id

                    tache['round_financing_and_foundation']['round_financing_id'] = meta_sub_project_entity. \
                        round_financing_and_Foundation_ids[0].round_financing_id.id

                    tache['round_financing_and_foundation']['the_amount_of_investment'] =  meta_sub_project_entity. \
                        round_financing_and_Foundation_ids[0].the_amount_of_investment

                    tache['round_financing_and_foundation']['ownership_interest'] = meta_sub_project_entity. \
                        round_financing_and_Foundation_ids[0].ownership_interest

                    tache['round_financing_and_foundation']['the_amount_of_financing'] = meta_sub_project_entity. \
                        round_financing_and_Foundation_ids[0].the_amount_of_financing

                    # -------------->

                    # 2 ------->   共享的子工程实例  可能为空,不过odoo特性很良好
                    # 运用odoo的特性可以非常好的使用空实体的问题
                    tache['sub_project'] = {}
                    tache['sub_project']['sub_project_id'] = meta_sub_project_entity.sub_project_ids.id
                    tache['sub_project']['name'] = meta_sub_project_entity.sub_project_ids.name
                    tache['sub_project']['project_number'] = meta_sub_project_entity.sub_project_ids.project_number
                    tache['sub_project']['invest_manager_id'] = meta_sub_project_entity.sub_project_ids.invest_manager_id.id





                    # tache['examine_and_verify'] = tache.examine_and_verify
                    tache['view_or_launch'] = sub_tache.view_or_launch
                    tache['meta_sub_project_id'] = meta_sub_project_entity.id
                    tache['sub_project_id'] = meta_sub_project_entity.sub_project_ids.id
                    # 当前子工程 只从的得到的主配置和子配置的内存实例去做数据的改变, 并不影响数据库中is_unlocked的值

                    # 由于原始环节可能对应多个自环节实体,  原因在于:  有多个元子工程  每个子工程对应一组子环节实体
                    # 不过在于子环节数据的获取是从元子工程的角度来获取
                    tache_entity = sub_tache.get_tache()

                    parent_entity = tache_entity.parent_id

                    if parent_entity.model_id.model_name == self._name:
                        tache['is_unlocked'] = parent_entity.is_unlocked
                    else:

                        # 考虑到主环节可以对应多个子环节(如果没有在元子工程的识别情况下)
                        parent_status_entitys = parent_entity.tache_status_id

                        parent_status_entity = None
                        for status_entity in parent_status_entitys:
                            if status_entity.meta_sub_project_id.id == meta_sub_project_entity.id:
                                parent_status_entity = status_entity
                                break


                        tache['is_unlocked'] = parent_status_entity.is_unlocked

                    break


        return process['stage_ids']



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


    # 查看或者发起
    def view_or_launch(self, **kwargs):
        '''
            总体分为两大类: 查看  发起
            字典中的key view_or_launch
                view_or_launch: True    查看
                view_or_launch: False   发起

            tache_id : 环节id

        :param kwargs:
        :return:
        '''

        ''' 
            参数1 : sub_project   轮次基金所在的子工程
            参数2 : view_or_launch   发起或者查看
            参数1 : sub_project   轮次基金所在的子工程
        '''

        # 刚开始的情况下,没有子工程
        # 理论上,只能有发起子工程 或者是查看主工程的事件操作
        if not kwargs.get('sub_project_id'):
            # 查看主工程
            if kwargs.get('view_or_launch'):
                return self._get_info()
            # 发起子工程
            else:
                tache_id = int(kwargs.get('tache_id'))
                tache_entity = self.process_id.get_tache_entity(tache_id)
                model_name = tache_entity.model_id.name
                # self.env[model_name]


            # 在这种情况下,就只有查看主project的操作
            return self._get_info()

        # 在有子工程的情况下,需要根据子工程,而且子工程的子配置信息
        # 也可以获取到
        else:
            sub_project_id = int(kwargs.get('sub_project_id'))


        #
        #     tache_id = int(kwargs.get('tache_id'))
        #     tache_entities = self.process_id.get_all_tache_entities()
        #     tache_target = None
        #     for tache in tache_entities:
        #         if tache.id == tache_id:
        #             tache_target = tache
        #             break
        #
        #     if kwargs.get('view_or_launch'):
        #         if tache_target.model_name == self._name:
        #             return self._get_info()
        #         else:
        #             # 拿到子工程 子配置的信息
        #             tache_status = tache_target.tache_status_id
        #             # tache_status.
        #
        #     else:
        #         pass
        #
        #     if tache_target.model_name == self._name:
        #
        #
        #
        # else:
        #     sup_project_id = int(kwargs.get('sub_project'))
        #
        #
        #     # 如果代表的是查看
        #     if kwargs.get('view_or_launch') == True:
        #         tache_entities = self.process_id.get_all_tache_entities()
        #         tache_target = None
        #         for tache in tache_entities:
        #             if tache.id == kwargs.get('tache_id'):
        #                 tache_target = tache
        #                 break
        #
        #
        #
        #         if tache_target.model_name == self._name:
        #             # 这种情况指的是主project的实体,所以就可以直接返回
        #             return self._get_info()
        #         else:
        #             tache_status = tache_target.tache_status_id
        #
        #
        #     # 这种情况则是代表着发起
        #     else:
        #         pass













