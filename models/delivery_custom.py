# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class ProviderNowCustom(models.Model):
    _inherit = 'delivery.carrier'

    delivery_type = fields.Selection(selection_add=[
        ('nowcustom', 'NOW Custom')
    ], ondelete={'nowcustom': lambda recs: recs.write({'delivery_type': 'fixed', 'fixed_price': 0})})


    def nowcustom_rate_shipment(self, order):
        self.ensure_one()

        price = 0.0
        return {'success': False,
                'price': price,
                'error_message': "We will contact you",
                'warning_message': False}