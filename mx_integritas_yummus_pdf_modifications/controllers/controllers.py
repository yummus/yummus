# -*- coding: utf-8 -*-
# from odoo import http


# class MxIntegritasYummusPdfModifications(http.Controller):
#     @http.route('/mx_integritas_yummus_pdf_modifications/mx_integritas_yummus_pdf_modifications/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mx_integritas_yummus_pdf_modifications/mx_integritas_yummus_pdf_modifications/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mx_integritas_yummus_pdf_modifications.listing', {
#             'root': '/mx_integritas_yummus_pdf_modifications/mx_integritas_yummus_pdf_modifications',
#             'objects': http.request.env['mx_integritas_yummus_pdf_modifications.mx_integritas_yummus_pdf_modifications'].search([]),
#         })

#     @http.route('/mx_integritas_yummus_pdf_modifications/mx_integritas_yummus_pdf_modifications/objects/<model("mx_integritas_yummus_pdf_modifications.mx_integritas_yummus_pdf_modifications"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mx_integritas_yummus_pdf_modifications.object', {
#             'object': obj
#         })
