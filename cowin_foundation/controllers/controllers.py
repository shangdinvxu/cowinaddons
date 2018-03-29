# -*- coding: utf-8 -*-
from odoo import http

# class CowinFoudation(http.Controller):
#     @http.route('/cowin_foundation/cowin_foundation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cowin_foundation/cowin_foundation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cowin_foundation.listing', {
#             'root': '/cowin_foundation/cowin_foundation',
#             'objects': http.request.env['cowin_foundation.cowin_foundation'].search([]),
#         })

#     @http.route('/cowin_foundation/cowin_foundation/objects/<model("cowin_foundation.cowin_foundation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cowin_foundation.object', {
#             'object': obj
#         })