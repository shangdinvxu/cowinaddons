# -*- coding: utf-8 -*-
from odoo import http

# class CowinPlugin(http.Controller):
#     @http.route('/cowin_plugin/cowin_plugin/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cowin_plugin/cowin_plugin/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cowin_plugin.listing', {
#             'root': '/cowin_plugin/cowin_plugin',
#             'objects': http.request.env['cowin_plugin.cowin_plugin'].search([]),
#         })

#     @http.route('/cowin_plugin/cowin_plugin/objects/<model("cowin_plugin.cowin_plugin"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cowin_plugin.object', {
#             'object': obj
#         })