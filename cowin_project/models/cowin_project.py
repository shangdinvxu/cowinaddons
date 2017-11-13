# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.modules.module import get_module_resource
from odoo import tools
import copy

class Cowin_project(models.Model):
    _name = 'cowin_project.cowin_project'

    @api.model
    def _default_image(self):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    # 关联到settings中,把该字段看成配置选项的操作
    process_id = fields.Many2one('cowin_project.process', ondelete="cascade")
    sub_project_ids = fields.One2many('cowin_project.cowin_subproject', 'project_id', string=u'子工程')

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




    @api.model
    def create(self, vals):
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
    def process_settings2(self, sub_project_id):
        '''

        :param sub_project_id: 子工程实例id
        :return:
        '''

        # 待处理的proces信息
        process = self.process_id.get_info()

        sub_project_entity = None
        # 代表着第一次默认选择第一个来显示,当然,如果存在的情况下
        # 返回给客户的时候页面需要默认显示的一条轮次基金数据
        if not sub_project_id:
            '''意思在于如果主工程子工程数据,那就显示子工程数据,否则就返回为空'''
            sub_project_entity = self.sub_project_ids

            # 第一条数据存在
            if sub_project_entity:
                sub_project_entity = sub_project_entity[0]

        else:
            for r_and_f in self.sub_project_ids:
                if r_and_f.id == sub_project_id:
                    sub_project_entity = r_and_f



        # 代表当前存在某个sub_project实体记录
        if sub_project_entity:
            # 该工程所有关联的环节状态的信息
            tache_status_entities = sub_project_entity.get_all_sub_tache_status()

            for tache_status in tache_status_entities:
                for stage in process['stage_ids']:
                    for tache in stage['tache_ids']:
                        if tache['id'] == tache_status.id:
                            # tache['examine_and_verify'] = tache.examine_and_verify
                            tache['view_or_launch'] = tache_status.view_or_launch
                            # 当前子工程 只从的得到的主配置和子配置的内存实例去做数据的改变, 并不影响数据库中is_unlocked的值

                            tache_entity = tache_status.get_tache()

                            parent_entity = tache_entity.parent_id

                            if parent_entity.model_id.name == self._name:
                                tache['is_unlocked'] = parent_entity.is_unlocked
                            else:
                                parent_status_entity = parent_entity.tache_status_id
                                tache['is_unlocked'] = parent_status_entity.is_unlocked

                            break

        # 如果当前没有工程,需要开启第二个环节的调条件 特殊情况,特殊对待
        else:
            stages = process['stage_ids'][1]
            tache2 = stages['tache_ids'][0]
            tache2['is_unlocked'] = True




        return process['stage_ids']



    # 获得每个project的详细信息
    def _get_info(self, round_financing_and_foundation_id=None):

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
                'process': self.process_settings2(round_financing_and_foundation_id),
                }



    def get_all_investment_funds(self):
        return [funds for funds in self.investment_funds]

    # 获得该项目中投资基金所在的投资轮次, 相当于子工程 sub_project
    def get_investment_funds(self):

        res = []
        count = 0

        # 获得所有的子工程
        sub_projects = self.sub_project_ids

        # 如果没有相应的实例,就直接返回
        if not sub_projects:
            return res

        # 如果有实例的情况
        for sub_pro in sub_projects:
            # 理论上只有一条记录 轮次_基金 finish状态 实例
            round_financing_and_foundation_entity = sub_pro.get_round_financing_and_foundation()

            # 输入 轮次基金id -->  res[i] (i需要的索引)

            found = False
            for i, round_financing_dict in enumerate(res):
                if round_financing_dict.get('round_financing_id') == round_financing_and_foundation_entity.\
                        round_financing_id.id:

                    round_financing_dict['foundation_names'].append({
                        'foundation_id': round_financing_and_foundation_entity.foundation_id.id,
                        'foundation_name': round_financing_and_foundation_entity.foundation_id.name,
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
                    }],
                })

                count += 1


        return res





    # 通过rpc调用,把详细的信息传递到前端以便于显示操作
    def rpc_get_info(self):
        return self._get_info()


    # 查看或者发起
    def view_or_launch(self, **kwargs):
        '''
            总体分为两大类: 查看  发起
            字典中的key view_or_launch
            view_or_launch: True  查看
            view_or_launch: False  发起
        :param kwargs:
        :return:
        '''

        pass




