# -*- coding: utf-8 -*-
from odoo import http

# class CowinInvestmentProject(http.Controller):
#     @http.route('/cowin_investment_project/cowin_investment_project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cowin_investment_project/cowin_investment_project/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cowin_investment_project.listing', {
#             'root': '/cowin_investment_project/cowin_investment_project',
#             'objects': http.request.env['cowin_investment_project.cowin_investment_project'].search([]),
#         })

#     @http.route('/cowin_investment_project/cowin_investment_project/objects/<model("cowin_investment_project.cowin_investment_project"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cowin_investment_project.object', {
#             'object': obj
#         })