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
        if not vals.get('project_number'):
            vals['project_number'] = self.env['ir.sequence'].next_by_code('cowin_project.order')

        if not vals.get('process_id'):
            meta_setting_entity = self.env['cowin_settings.process'].search([('category', '=', 'init_preinvestment')])

            # 每次创建的实例 都要从数据
            process = self.env['cowin_project.process'].create_process_info(meta_setting_entity.copy_custom(),
                                                                            meta_setting_entity.id)

            vals['process_id'] = process.id


        return super(Cowin_project, self).create(vals)




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


    # 用来处理每个基金投资阶段中settings配置信息的改变
    # f_stage 基金状态记录
    def process_settings(self, f_stage_id):
        # 获得基础的配置信息
        stages = self.process_id.get_info()['stage_ids']
        stages = copy.deepcopy(stages)
        # 深拷贝的目的在于不让数据产生干扰,因为stages是公共数据
        for stage in stages:
            for tache in stage['tache_ids']:
                if tache['model_name'] == self._name:
                    examine_and_verify = self.examine_and_verify
                    view_or_launch = True
                else:
                    model_name = tache['model_name']
                    target = self.env[model_name].search([('foundation_stage_id', '=', f_stage_id)])
                    examine_and_verify = target.examine_and_verify
                    view_or_launch = True if target else False

                tache['examine_and_verify'] = examine_and_verify
                tache['view_or_launch'] = view_or_launch

        return stages

    def process_settings2(self, round_financing_and_foundation_id):
        '''

        :param round_financing_and_foundation_id: 轮次基金实体id
        :return:
        '''

        # 待处理的proces信息
        process = self.process_id.get_info()

        res = {}

        round_financing_and_foundation = None
        # 代表着第一次默认选择第一个来显示,当然,如果存在的情况下
        if not round_financing_and_foundation_id:
            round_financing_and_foundations = self.round_financing.round_financing_for_foundation_ids
            # 第一条数据存在
            if round_financing_and_foundations:
                round_financing_and_foundation = round_financing_and_foundations[0]

        else:
            round_financing_and_foundation = self.round_financing.browse(round_financing_and_foundation_id)


        # 代表当前存在某个基金环节实体记录
        if round_financing_and_foundation:

            # 或得到当前的基金环节记录实体
            for stage in process['stage_ids']:
                for tache in stage['tache_ids']:
                    if tache['model_name'] == self._name:
                        examine_and_verify = self.examine_and_verify
                        view_or_launch = True
                    else:
                        model_name = tache['model_name']
                        target = self.env[model_name].search([('foundation_stage_id', '=', round_financing_and_foundation.id)])
                        examine_and_verify = target.examine_and_verify
                        view_or_launch = True if target else False

                    tache['examine_and_verify'] = examine_and_verify
                    tache['view_or_launch'] = view_or_launch

        # 如果当前没有任何基金,只需要能够显示project的状态信息
        else:
            for stage in process['stage_ids']:
                for tache in stage['tache_ids']:
                    if tache['model_name'] == self._name:
                        examine_and_verify = self.examine_and_verify
                        view_or_launch = True
                        tache['examine_and_verify'] = examine_and_verify
                        tache['view_or_launch'] = view_or_launch

                        break

        return process['stage_ids']







    def get_investment_funds2(self):

        # 1 构建 轮次 --> index 索引
        look_up_table = {}
        count = 0
        res = []

        foundations = self.get_all_investment_funds()
        # 某些情况下基金并没有构建起来
        if not foundations:
            # 获得基础的配置信息
            stages = self.process_id.get_info()['stage_ids']
            stages = copy.deepcopy(stages)
            for stage in stages:
                for tache in stage['tache_ids']:
                    if tache['model_name'] == self._name:
                        examine_and_verify = self.examine_and_verify
                        view_or_launch = True
                    else:
                        # model_name = tache['model_name']
                        # target = self.env[model_name].search([('foundation_stage_id', '=', f_stage.id)])
                        examine_and_verify = False
                        view_or_launch = False

                    tache['examine_and_verify'] = examine_and_verify
                    tache['view_or_launch'] = view_or_launch

            res.append({})
            res[0]['round_financing'] = u''
            res[0]['foudation_stages'] = []
            res[0]['foudation_stages'].append({
                'foudation_stage_id': -1,
                'name': u'',
                'process': stages
            })


        else:

            for foundation in foundations:
                f_stages = foundation.get_all_stage()

                for f_stage in f_stages:
                    # 融资轮次
                    round_financing_name = f_stage.round_financing.name
                    # 切记,这里要关注的是返回None的值的序列
                    if look_up_table.get(round_financing_name) is None:
                        i = look_up_table[round_financing_name] = count
                        res.append({})
                        # 融资轮次
                        res[i]['round_financing'] = round_financing_name
                        # 融资基金
                        res[i]['foudation_stages'] = []
                        count += 1
                    index = look_up_table[round_financing_name]
                    res[index]['foudation_stages'].append({
                        'foudation_stage_id': f_stage.id,
                        'name': f_stage.foudation_id.name,
                        # 'process': self.process_settings(f_stage)
                    })

        return res



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

    def get_default_display_foundation_stage(self):
        if self.investment_funds:
            fundation_stage = self.investment_funds[0][0]
            taches = self.process_id.get_all_taches()
            res = []
            for tache in taches:

                if tache['model_name'] == self._name:
                    view_or_launch = True
                    examine_and_verify = self.examine_and_verify
                else:

                    target = self.env[tache['model_name']].search([('foundation_stage_id', '=', fundation_stage.id)])
                    view_or_launch = True if target else False
                    examine_and_verify = target.examine_and_verify

                once_or_more = tache['once_or_more']

                res.append({
                    'tache_id': tache['id'],
                    'examine_and_verify': examine_and_verify,
                    'view_or_launch': view_or_launch,
                    'once_or_more': once_or_more,

                })

            return res



    def rpc_select_dislay_foundation(self, foundation_stage_id):

        fundation_stage = self.env['cowin_foudation.cowin_foudation_stage'].browse(int(foundation_stage_id))
        taches = self.process_id.get_all_taches()
        res = []
        for tache in taches:
            examine_and_verify = tache.examine_and_verify
            if tache.model_name == self._name:
                view_or_launch = True
            else:
                target = self.env[tache.model_name].search([('foundation_stage_id',
                                                             '=', fundation_stage.id)])
                view_or_launch = True if target else False

            once_or_more = tache.once_or_more

            res.append({
                'tache_id': tache.id,
                'examine_and_verify': examine_and_verify,
                'view_or_launch': view_or_launch,
                'once_or_more': once_or_more,

            })

        result = self._get_info()
        result['select_display_foundation'] = res
        return result


    def get_all_investment_funds(self):
        return [funds for funds in self.investment_funds]

        # 获得该项目中投资基金所在的投资轮次,
    def get_investment_funds(self):

        res = []

        # 拿到所有的轮次
        round_financings = self.env['cowin_common.round_financing'].search([])

        for round_financing in round_financings:
            # 拿到所有的基金
            current = {
                'round_financing_id': round_financing.id,
                'round_financing_name': round_financing.name,
                'foundations': []
            }
            for foundation in round_financing.round_financing_for_foundation_ids:
                current['foundations'].append({
                    'foundation_id': foundation.id,
                    'foundation_name': foundation.name,
                })

            res.append(current)


        return res





    # 通过rpc调用,把详细的信息传递到前端以便于显示操作
    def rpc_get_info(self):
        return self._get_info()