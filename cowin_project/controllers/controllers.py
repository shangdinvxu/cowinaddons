# -*- coding: utf-8 -*-
# from odoo import http

# class CowinProject(http.Controller):
#     @http.route('/cowin_project/cowin_project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

    # @http.route('/cowin_project/cowin_project/objects/', auth='public')
    # def list(self, **kw):
    #     return http.request.render('cowin_project.listing', {
    #         'root': '/cowin_project/cowin_project',
    #         'objects': http.request.env['cowin_project.cowin_project'].search([]),
    #     })

    # @http.route('/cowin_project/cowin_project/objects/<model("cowin_project.cowin_project"):obj>/', auth='public')
    # def object(self, obj, **kw):
    #     return http.request.render('cowin_project.object', {
    #         'object': obj
    #     })