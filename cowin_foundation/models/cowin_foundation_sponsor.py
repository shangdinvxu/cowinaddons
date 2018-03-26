# -*- coding: utf-8 -*-


from odoo import models, fields, api


class Cowin_foundation_sponsor(models.Model):
    _name = 'cowin_foudation.sponsor'

    '''
        出资人信息
    '''

    name = fields.Char(string=u'出资人名称')

    foundation_id = fields.Many2one('cowin_foundation.cowin_foundation', string=u'基金', ondelete='cascade')

    registered_address = fields.Char(string=u'注册地址')

    capital_contribution = fields.Float(string=u'出资金额(万元)')

    capital_ratio = fields.Float(string=u'出资比例')

    amount_of_payment = fields.Float(string=u'实缴金额(万元)')

    amount_of_payment_ratio = fields.Float(string=u'实缴比例')

    the_nature_of_the_investor = fields.Selection([(1, u'国有'), (2, u'民营'), (3, u'外资')], string=u'出资人性质')

    institutional_investor = fields.Selection([(1, u'是'), (0, u'不是')], string=u'是否为投资机构')

    mailing_address_of_shareholders = fields.Char(string=u'股东邮寄地址')

    contract_person = fields.Char(string=u'联系人')

    contract_phone = fields.Char(string=u'联系电话')

    ID_number = fields.Char(string=u'证件号码')

    contract_email = fields.Char(string=u'Email')


    _sql_constraints = [
        ('name_key', 'UNIQUE (name)', u'出资人名称不能够相同')
    ]

    # 获得出资人的列表的信息
    @api.multi
    def get_sponsor_info(self):
        # 构建自定义的many2many数据存储
        res = []
        for rec in self:
            tmp = {}
            tmp['form_id'] = self.get_formview_id()
            for k in rec._fields:
                if rec._fields[k].type in ('many2many', 'one2many', 'many2one'):
                    tmp[k] = rec[k].read(['name'])

                elif rec._fields[k].type == 'selection':
                    kk = rec[k]
                    selection = rec._fields[k].selection
                    vv = filter(lambda t: t[0] == kk, selection) # 理论上只会由一个
                    tmp[k] = vv[0][1] if vv else False  #  vv可以为空 (index, '描述')


                else:
                    tmp[k] = rec[k]

            res.append(tmp)

        return res