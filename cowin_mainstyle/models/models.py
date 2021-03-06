# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class cowin_mainstyle(models.Model):
#     _name = 'cowin_mainstyle.cowin_mainstyle'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


class IrMenuExtend(models.Model):
    _inherit = 'ir.ui.menu'

    button_icon = fields.Char(string=u'按钮图标')

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        fields.append("button_icon")
        return super(IrMenuExtend, self).read(fields, load)