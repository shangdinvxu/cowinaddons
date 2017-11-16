# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Cowin_project_subproject_call_up_record(models.Model):
    '''
        尽调拜访记录
    '''

    _name = 'cowin_project.sub_call_up_record'

    # foundation_stage_id = fields.Many2one('cowin_foudation.cowin_foudation_stage', string=u'基金阶段')


    subproject_id = fields.Many2one('cowin_project.cowin_subproject')

    name = fields.Char(related='subproject_id.name', string=u"项目名称")
    project_number = fields.Char(related='subproject_id.project_number', string=u'项目编号')
    invest_manager_id = fields.Many2one('hr.employee', related='subproject_id.invest_manager_id', string=u'投资经理')

    visit_date = fields.Date(string=u'拜访日期')

    customer_type = fields.Many2one('', string=u'客户类型')

    customer_name = fields.Char(string=u'姓名')
    customer_position = fields.Char(string=u'职位')
    customer_contract = fields.Char(string=u'联系方式')
    customer_email = fields.Char(string=u'Email')
    customer_company_name = fields.Char(string=u'公司名称')
    customer_relation_investment = fields.Char(string=u'与拟投资项目关系')
    customer_relation_value = fields.Text(string=u'对拟投资项目评价')
    customer_relation_opinion = fields.Text(string=u'意见或建议')
    recommended_visit_object = fields.Char(string=u'其它推荐拜访对象')


    # round_financing_and_foundation_id = fields.Many2one('cowin_project.round_financing_and_foundation',
    #                                                     string=u'环节和基金整体')



    @api.model
    def create(self, vals):
        tache = self._context['tache']

        sub_project_id = int(tache['sub_project_id'])

        # vals['meta_sub_project_id'] = meta_sub_project_id

        sub_tache_id = int(tache['sub_tache_id'])

        sub_tache = self.env['cowin_project.subproject_process_tache'].browse(sub_tache_id)

        vals['subproject_id'] = sub_project_id
        res = super(Cowin_project_subproject_call_up_record, self).create(vals)
        sub_tache.write({
            'res_id': res.id,
            'is_unlocked': True,
            'view_or_launch': True,
        })

        return res

