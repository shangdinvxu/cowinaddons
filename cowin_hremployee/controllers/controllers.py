# -*- coding: utf-8 -*-
from odoo import http

# class CowinHremployee(http.Controller):
#     @http.route('/cowin_hremployee/cowin_hremployee/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cowin_hremployee/cowin_hremployee/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cowin_hremployee.listing', {
#             'root': '/cowin_hremployee/cowin_hremployee',
#             'objects': http.request.env['cowin_hremployee.cowin_hremployee'].search([]),
#         })

#     @http.route('/cowin_hremployee/cowin_hremployee/objects/<model("cowin_hremployee.cowin_hremployee"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cowin_hremployee.object', {
#             'object': obj
#         })