# -*- coding: utf-8 -*-
from odoo import http

# class CowinFoudation(http.Controller):
#     @http.route('/cowin_foudation/cowin_foudation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cowin_foudation/cowin_foudation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cowin_foudation.listing', {
#             'root': '/cowin_foudation/cowin_foudation',
#             'objects': http.request.env['cowin_foudation.cowin_foudation'].search([]),
#         })

#     @http.route('/cowin_foudation/cowin_foudation/objects/<model("cowin_foudation.cowin_foudation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cowin_foudation.object', {
#             'object': obj
#         })