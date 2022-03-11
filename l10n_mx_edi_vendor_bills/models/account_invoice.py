# Copyright 2017, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
from codecs import BOM_UTF8

from odoo import _, api, models, fields

BOM_UTF8U = BOM_UTF8.decode('UTF-8')
CFDI_SAT_QR_STATE = {
    'No Encontrado': 'not_found',
    'Cancelado': 'cancelled',
    'Vigente': 'valid',
}


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    #l10n_mx_edi_cfdi = fields.Binary(
    #    'CFDI content', copy=False, readonly=True,
    #    help='The cfdi xml content encoded in base64.',
    #    compute='_compute_cfdi_values')
    def generate_edi_document(self,attach):
        self.ensure_one()
        reg={'move_id':self.id,
            'attachment_id':attach.id,
            'edi_format_id':self.env.ref('l10n_mx_edi.edi_cfdi_3_3').id,
            'state':'sent' }
        self.env['account.edi.document'].create(reg)

    def generate_xml_attachment(self,l10n_mx_edi_cfdi):
        self.ensure_one()
        if not l10n_mx_edi_cfdi:
            return False
        print(l10n_mx_edi_cfdi)
        fname = ("%s-%s-MX-Bill-%s.xml" % (
            self.journal_id.code, self.ref,
            self.company_id.partner_id.vat or '')).replace('/', '')
        data_attach = {
            'name': fname,
            'datas': base64.encodebytes(l10n_mx_edi_cfdi),
            #'datas_fname': 'fname',
            'description': _('XML signed from Invoice %s.') % fname,
            'res_model': self._name,
            'res_id': self.id,
        }
        #self.l10n_mx_edi_cfdi_name = fname
        return self.env['ir.attachment'].with_context({}).create(data_attach)


    def create_adjustment_line(self, xml_amount):
        """If the invoice has difference with the total in the CFDI is
        generated a new line with that adjustment if is found the account to
        assign in this lines. The account is assigned in a system parameter
        called 'adjustment_line_account_MX'"""
        account_id = self.env['ir.config_parameter'].sudo().get_param(
            'adjustment_line_account_MX', '')
        if not account_id:
            return False
        self.invoice_line_ids.create({
            'account_id': account_id,
            'name': _('Adjustment line'),
            'quantity': 1,
            'price_unit': xml_amount - self.amount_total,
            'invoice_id': self.id,
        })
        return True
    

    def l10n_mx_edi_get_tfd_etree(self, cfdi):
        '''Get the TimbreFiscalDigital node from the cfdi.
        :param cfdi: The cfdi as etree
        :return: the TimbreFiscalDigital node
        '''
        if not hasattr(cfdi, 'Complemento'):
            return None
        attribute = 'tfd:TimbreFiscalDigital[1]'
        namespace = {'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'}
        node = cfdi.Complemento.xpath(attribute, namespaces=namespace)
        return node[0] if node else None
