# -*- coding: utf-8 -*-
from odoo import api, models, fields, tools, _

class AccountEdiFormat(models.Model):
    _inherit = 'account.edi.format'

    def _post_invoice_edi(self, invoices, test_mode=False):
        for invoice in invoices:
            if invoice.edi_document_ids:
                for edidoc in invoice.edi_document_ids:
                    if edidoc.state=='sent':
                        print("Factura Nula Timbrada")
                        return {}
        return super()._post_invoice_edi(invoices, test_mode=test_mode)
    
    def _is_required_for_invoice(self, invoice):
        self.ensure_one()
        if invoice.edi_document_ids:
            for doc in invoice.edi_document_ids:
                if doc.state=='sent':
                    return False
        return super()._is_required_for_invoice(invoice)