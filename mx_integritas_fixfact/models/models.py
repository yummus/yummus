# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class mx_integritas_fixfact(models.Model):
#     _name = 'mx_integritas_fixfact.mx_integritas_fixfact'
#     _description = 'mx_integritas_fixfact.mx_integritas_fixfact'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
