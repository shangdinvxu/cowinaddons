# -*- encoding: utf-8 -*-
from openerp import http
from openerp.http import request, local_redirect
from openerp.addons.web.controllers.main import Home
from openerp.addons.website.controllers.main import Website


class Home(Home):
    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        request.params['disable_footer'] = True
        request.params['disable_database_manager'] = True
        request.params['background_src'] = '/cowin_mainstyle/static/src/img/login_bg.jpg'
        images = request.env['hr.employee'].sudo().search([])
        list = []
        for img in images:
            list.append(img.image_medium)
        request.params['images'] = list

        resp = super(Home, self).web_login(redirect, **kw)
        if resp.qcontext.get('error') == u'Wrong login/password':
            resp.qcontext['error'] = u'用户名或密码错误'
        return resp

#
class Website(Website):
    @http.route('/', auth='public')
    def index(self, **kw):
        return local_redirect('/web')