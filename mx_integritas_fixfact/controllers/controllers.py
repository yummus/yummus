# -*- coding: utf-8 -*-
# from odoo import http


# class MxIntegritasFixfact(http.Controller):
#     @http.route('/mx_integritas_fixfact/mx_integritas_fixfact/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mx_integritas_fixfact/mx_integritas_fixfact/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mx_integritas_fixfact.listing', {
#             'root': '/mx_integritas_fixfact/mx_integritas_fixfact',
#             'objects': http.request.env['mx_integritas_fixfact.mx_integritas_fixfact'].search([]),
#         })

#     @http.route('/mx_integritas_fixfact/mx_integritas_fixfact/objects/<model("mx_integritas_fixfact.mx_integritas_fixfact"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mx_integritas_fixfact.object', {
#             'object': obj
#         })
