# -*- coding: utf-8 -*-
from odoo import http

# class CowinMainstyle(http.Controller):
#     @http.route('/cowin_mainstyle/cowin_mainstyle/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cowin_mainstyle/cowin_mainstyle/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cowin_mainstyle.listing', {
#             'root': '/cowin_mainstyle/cowin_mainstyle',
#             'objects': http.request.env['cowin_mainstyle.cowin_mainstyle'].search([]),
#         })

#     @http.route('/cowin_mainstyle/cowin_mainstyle/objects/<model("cowin_mainstyle.cowin_mainstyle"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cowin_mainstyle.object', {
#             'object': obj
#         })