# -*- coding: utf-8 -*-
from odoo import http

# class CowinCore(http.Controller):
#     @http.route('/cowin_core/cowin_core/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cowin_core/cowin_core/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cowin_core.listing', {
#             'root': '/cowin_core/cowin_core',
#             'objects': http.request.env['cowin_core.cowin_core'].search([]),
#         })

#     @http.route('/cowin_core/cowin_core/objects/<model("cowin_core.cowin_core"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cowin_core.object', {
#             'object': obj
#         })