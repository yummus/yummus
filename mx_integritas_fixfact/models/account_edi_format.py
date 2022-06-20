# -*- coding: utf-8 -*-
from odoo import api, models, fields, tools, _
from odoo.tools.xml_utils import _check_with_xsd
from odoo.tools.float_utils import float_round, float_is_zero

import logging
import re
import base64
import json
import requests
import random
import string

from lxml import etree
from lxml.objectify import fromstring
from datetime import datetime
from io import BytesIO
from zeep import Client
from zeep.transports import Transport
from json.decoder import JSONDecodeError

_logger = logging.getLogger(__name__)


class AccountEdiFormat(models.Model):
    _inherit = "account.edi.format"

    def _l10n_mx_edi_get_invoice_line_cfdi_values(self, invoice, line):
        cfdi_values = {"line": line}

        # ==== Amounts ====

        cfdi_values["price_unit_wo_discount"] = line.price_unit * (
            1 - (line.discount / 100.0)
        )

        if line.discount != 100.0:
            gross_price_subtotal = invoice.currency_id.round(
                line.price_subtotal / (1 - line.discount / 100.0)
            )
        else:
            gross_price_subtotal = invoice.currency_id.round(
                line.price_unit * line.quantity
            )
        cfdi_values["discount_amount"] = gross_price_subtotal - line.price_subtotal
        cfdi_values["total_wo_discount"] = gross_price_subtotal
        cfdi_values["price_subtotal_unit"] = (
            invoice.currency_id.round(cfdi_values["total_wo_discount"] / line.quantity)
            if line.quantity
            else 0
        )

        # ==== Taxes ====

        tax_details = line.tax_ids.compute_all(
            cfdi_values["price_unit_wo_discount"],
            currency=line.currency_id,
            quantity=line.quantity,
            product=line.product_id,
            partner=line.partner_id,
            is_refund=invoice.move_type in ("out_refund", "in_refund"),
        )

        cfdi_values["tax_details"] = {}
        for tax_res in tax_details["taxes"]:
            if tax_res["base"] == 0:
                continue
            tax = self.env["account.tax"].browse(tax_res["id"])

            tax_rep_field = (
                "invoice_repartition_line_ids"
                if invoice.move_type == "out_invoice"
                else "refund_repartition_line_ids"
            )
            tags = tax[tax_rep_field].tag_ids
            tax_name = (
                {"ISR": "001", "IVA": "002", "IEPS": "003"}.get(tags.name)
                if len(tags) == 1
                else None
            )

            cfdi_values["tax_details"].setdefault(
                tax,
                {
                    "tax": tax,
                    "base": tax_res["base"],
                    "tax_type": tax.l10n_mx_tax_type,
                    "tax_amount": tax.amount / 100.0
                    if tax.amount_type != "fixed"
                    else tax.amount / tax_res["base"],
                    "tax_name": tax_name,
                    "total": 0.0,
                },
            )

            cfdi_values["tax_details"][tax]["total"] = tax_res["amount"]

        cfdi_values["tax_details"] = list(cfdi_values["tax_details"].values())
        cfdi_values["tax_details_transferred"] = [
            tax_res
            for tax_res in cfdi_values["tax_details"]
            if tax_res["tax_amount"] >= 0.0
        ]
        cfdi_values["tax_details_withholding"] = [
            tax_res
            for tax_res in cfdi_values["tax_details"]
            if tax_res["tax_amount"] < 0.0
        ]

        return cfdi_values
