# -*- coding: utf-8 -*-
from odoo import http

# class CowinSettings(http.Controller):
#     @http.route('/cowin_settings/cowin_settings/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cowin_settings/cowin_settings/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cowin_settings.listing', {
#             'root': '/cowin_settings/cowin_settings',
#             'objects': http.request.env['cowin_settings.cowin_settings'].search([]),
#         })

#     @http.route('/cowin_settings/cowin_settings/objects/<model("cowin_settings.cowin_settings"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cowin_settings.object', {
#             'object': obj
#         })