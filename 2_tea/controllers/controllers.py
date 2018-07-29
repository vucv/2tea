# -*- coding: utf-8 -*-
from openerp import http

# class 2Tea(http.Controller):
#     @http.route('/2_tea/2_tea/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/2_tea/2_tea/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('2_tea.listing', {
#             'root': '/2_tea/2_tea',
#             'objects': http.request.env['2_tea.2_tea'].search([]),
#         })

#     @http.route('/2_tea/2_tea/objects/<model("2_tea.2_tea"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('2_tea.object', {
#             'object': obj
#         })