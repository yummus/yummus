from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    
    def generate_xml_attachment(self,l10n_mx_edi_cfdi):
        self.ensure_one()
        res = super().generate_xml_attachment(l10n_mx_edi_cfdi)
        #version = self.l10n_mx_edi_get_pac_version()
        filename = ('%s-%s-MX-Invoice.xml' % (
                self.journal_id.code, self.name)).replace('/', '')
        print(res)
        print(filename)      
        res.name=filename
        #elf.l10n_mx_edi_cfdi_name=filename
        #print(self.l10n_mx_edi_cfdi_name)
        if self._context.get('l10n_mx_edi_invoice_type') == 'out':
            self.l10n_mx_edi_sat_status = 'valid'
        return res

    
    #def _l10n_mx_edi_retry(self):
    #    """avoid generate cfdi when the cfdi was attached"""
    #    to_retry_invoices = self.filtered(
    #        lambda inv: inv.l10n_mx_edi_pac_status != 'signed')
    #    return super(AccountInvoice, to_retry_invoices)._l10n_mx_edi_retry()

    
    def invoice_validate(self):
        attach_invoices = self.filtered(
            lambda inv:
            inv.state == 'draft' and inv.l10n_mx_edi_sat_status == 'valid')
        attachs = []
        for inv in attach_invoices:
            attachs.append((inv, inv.l10n_mx_edi_retrieve_last_attachment()))
        res = super().invoice_validate()
        #for inv, att in attachs:
        #    att.name = inv.l10n_mx_edi_cfdi_name
        return res
        
    def _l10n_mx_edi_retry(self):
        for fact in self:
            if fact.edi_document_ids:
                print("Ya Firmada")
                continue
            else:
                return super(AccountInvoice, self)._l10n_mx_edi_retry()
