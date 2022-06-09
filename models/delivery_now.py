# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ProviderNow(models.Model):
    _inherit = 'delivery.carrier'

    delivery_type = fields.Selection(selection_add=[
        ('noweu', 'NOW EU')
    ], ondelete={'noweu': lambda recs: recs.write({'delivery_type': 'fixed', 'fixed_price': 0})})

    def noweu_rate_shipment(self, order):
        ''' Compute the price of the order shipment
        :param order: record of sale.order
        :return dict: {'success': boolean,
                       'price': a float,
                       'error_message': a string containing an error message,
                       'warning_message': a string containing a warning message}
                       # TODO maybe the currency code?
        '''
        self.ensure_one()
        price = 23.00
        # if False:
        #     return {'success': False,
        #         'price': 0.0,
        #         'error_message': check_value,
        #         'warning_message': False}    

        return {'success': True,
                'price': price,
                'error_message': False,
                'warning_message': False} 