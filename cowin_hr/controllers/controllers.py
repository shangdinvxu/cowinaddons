# -*- coding: utf-8 -*-
from odoo import http

# class CowinHr(http.Controller):
#     @http.route('/cowin_hr/cowin_hr/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cowin_hr/cowin_hr/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cowin_hr.listing', {
#             'root': '/cowin_hr/cowin_hr',
#             'objects': http.request.env['cowin_hr.cowin_hr'].search([]),
#         })

#     @http.route('/cowin_hr/cowin_hr/objects/<model("cowin_hr.cowin_hr"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cowin_hr.object', {
#             'object': obj
#         })