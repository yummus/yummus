# -*- coding: utf-8 -*-
# from odoo import http


# class AmazonLogsAdded(http.Controller):
#     @http.route('/amazon_logs_added/amazon_logs_added', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/amazon_logs_added/amazon_logs_added/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('amazon_logs_added.listing', {
#             'root': '/amazon_logs_added/amazon_logs_added',
#             'objects': http.request.env['amazon_logs_added.amazon_logs_added'].search([]),
#         })

#     @http.route('/amazon_logs_added/amazon_logs_added/objects/<model("amazon_logs_added.amazon_logs_added"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('amazon_logs_added.object', {
#             'object': obj
#         })
