# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Cowin_subprojerct_prcess_tache_status(models.Model):
    _name = 'cowin_project.subproject_process_tache'


    '''
        每个子subproject都有自己的缓解状态信息
    '''


    name = fields.Char()

    tache_id = fields.Many2one('cowin_project.process_tache', string=u'环节')
    sub_project_id  = fields.Many2one('cowin_project.cowin_subproject', string=u'字工程名')


    # 这三条数据对应的是不同的子工程的使用,其他数据不会变更
    is_unlocked = fields.Boolean(string=u'是否已解锁', default=False)
    res_id = fields.Integer(string=u'该环节对应该实例另一个字段model_id中的一个实例')
    view_or_launch = fields.Boolean(string=u'发起或者新增', default=False)


    # ---->
    def get_tache(self):
        return self.tache_id