# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Node_Base(models.Model):
    _name = 'cowin_foudation.node_base'

    '''
        构建node_base节点,方便数据的级联删除
        
    '''


    name = fields.Char(string=u'基本节点的名称')


