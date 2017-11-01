# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.modules.module import get_module_resource
from odoo import tools


class Cowin_project(models.Model):
    _name = 'cowin_project.cowin_project'

    @api.model
    def _default_image(self):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    # 关联到settings中,把该字段看成配置选项的操作
    process_id = fields.Many2one('cowin_settings.process', ondelete="cascade", required=True)

    image = fields.Binary("LOGO", default=_default_image, attachment=True,
                          help="This field holds the image used as photo for the cowin_project, limited to 1024x1024px.")

    name = fields.Char(string=u"项目名称", required=True)

    project_number = fields.Char(string=u'项目编号',
                                 defualt=lambda self: self.env['ir.sequence'].next_by_code('cowin_project.order'))
    project_source = fields.Selection([(1, u'朋友介绍'), (2, u'企业自荐')],
                              string=u'项目来源', required=True)
    project_source_note = fields.Char(string=u'项目来源备注')
    invest_manager = fields.Many2one('hr.employee', string=u'投资经理')

    investment_funds = fields.One2many('cowin_project.cowin_foudation', 'project_id', string=u'投资基金')
    # investment_funds = fields.Many2one('cowin_project.cowin_foudation', string=u'投资基金')
    round_financing = fields.Many2one('cowin_project.round_financing', string=u'融资轮次')
    round_money = fields.Float(string=u'本次融资额')

    project_company_profile = fields.Text(string=u'项目公司概况')
    project_appraisal = fields.Text(string=u'项目评价')
    project_note = fields.Text(string=u'备注')
    industry = fields.Many2one('cowin_project.cowin_industry', string=u'所属行业')
    stage = fields.Selection([(1, u'种子期'), (2, u'成长早期'), (3, u'成长期'), (4, u'成熟期')], string=u'所属阶段', default=1)
    # stage = fields.Many2one('cowin_project.round_financing', string=u'融资轮次')
    production = fields.Text(string=u'产品')
    registered_address = fields.Char(string=u'注册地')
    peration_place = fields.Char(string=u'运营地')
    founding_time = fields.Date(string=u'成立时间')
    contract_person = fields.Char(string=u'联系人')
    contract_phone = fields.Char(string=u'联系电话')
    contract_email = fields.Char(string=u'Email')
    # attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=lambda self: [('res_model', '=', self._name)],
    #                                  auto_join=True, string=u"附件")

    attachment_ids = fields.Many2many('ir.attachment', string=u"附件")

    # displayed_image_id = fields.Many2one('ir.attachment', domain="[('res_model', '=', 'project.task'), ('res_id', '=', id), ('mimetype', 'ilike', 'image')]", string='Displayed Image')

    attachment_note = fields.Char(string=u'附件说明')



    #
    # @api.model
    # def create(self, vals):
    #     if not vals.get('project_number'):
    #         vals['project_number'] = self.env['ir.sequence'].next_by_code('cowin_project.order')
    #
    #     return super(Cowin_project, self).create(vals)



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
                    foudation = self.env['cowin_project.cowin_foudation'].browse(int(foudation_id))
                    foudation_stage_id = foudation.get_round_financing(round_financing).id
                    t = self.env[tache.model_name].search([('foudation_stage_id', '=', foudation_stage_id)]).id
            else:
                t = False
            temp.append({'tache_id': tache,
                         'model_name': tache.model_name,
                         'res_id': t
                         })

        return temp



    # 获得每个project的xiang详细信息
    def _get_info(self):
        # check_result = self._check_request_is_exist()

        return {'id': self.id,
                'name': self.name,
                'process_id': self.process_id.id,
                'image': self.image,
                'project_number': self.project_number,
                'project_source': self.project_source,
                'project_source_note': self.project_source_note,
                'invest_manager': self.invest_manager,
                'round_financing': self.round_financing,
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
                # 'attachment_ids': self.attachment_ids,
                'attachment_note': self.attachment_note,
                'process': self.process_id.get_info(),
                'investment_funds': self.get_investment_funds(),
                # 'check_view_status': self._check_view_status()
                }


    # 获得该项目中投资基金所在的投资轮次,
    def get_investment_funds(self):

        res = {}
        for investment_fund in self.investment_funds:
            stages = investment_fund.get_all_stage()
            for stage in stages:
                if not res.get(stage.round_financing):
                    res[stage.round_financing] = []
                res[stage.round_financing].append({
                    'foudation_id': investment_fund.id,
                    'foudation_name': investment_fund.name
                })


        # 根据基金的id来对数据进行排序操作
        for k, v in res.items():
            sorted(v, key=lambda x: x['foudation_id'])
            res[k] = v

        return res





    # 通过rpc调用,把详细的信息传递到前端以便于显示操作
    def rpc_get_info(self):
        return self._get_info()