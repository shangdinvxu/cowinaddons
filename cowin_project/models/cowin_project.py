from odoo import models, fields, api


class cowin_project(models.Model):
    _name = 'cowin_project.cowin_project'

    name = fields.Char(string=u'项目名称')

    project_number = fields.Char(string=u'项目编号')

    invest_manager = fields.Char(string=u'投资经理')

    project_partner = fields.Char(string=u'项目合伙人')

    registered_address = fields.Char(string=u'注册地')

    peration_place = fields.Char(string=u'运营地')

    contract_person = fields.Char(string=u'联系人')

    industry = fields.Char(string=u'所属行业')

    production = fields.Text(string=u'产品')

    register_person = fields.Char(string=u'登记人')

    state = fields.Char(string=u'状态')

    @api.model
    def create(self, vals):
        if not vals.get('project_number'):
            vals['project_number'] = self.env['ir.sequence'].next_by_code('cowin_project.order')

        return super(cowin_project, self).create(vals)
