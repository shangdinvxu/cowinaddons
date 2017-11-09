# -*- coding: utf-8 -*-
from odoo import http

# class CowinCommon(http.Controller):
#     @http.route('/cowin_common/cowin_common/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cowin_common/cowin_common/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cowin_common.listing', {
#             'root': '/cowin_common/cowin_common',
#             'objects': http.request.env['cowin_common.cowin_common'].search([]),
#         })

#     @http.route('/cowin_common/cowin_common/objects/<model("cowin_common.cowin_common"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cowin_common.object', {
#             'object': obj
#         })