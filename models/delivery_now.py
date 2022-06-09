
from odoo import api, fields, models, _

class ProviderNow(models.Model):
    _inherit = 'delivery.carrier'

    delivery_type = fields.Selection(selection_add=[
        ('now_eu', 'NOW EU')
    ], ondelete={'now_eu': lambda recs: recs.write({'delivery_type': 'fixed', 'fixed_price': 0})})

    def rate_shipment(self, order):
        ''' Compute the price of the order shipment
        :param order: record of sale.order
        :return dict: {'success': boolean,
                       'price': a float,
                       'error_message': a string containing an error message,
                       'warning_message': a string containing a warning message}
                       # TODO maybe the currency code?
        '''
        self.ensure_one()
        if hasattr(self, '%s_rate_shipment' % self.delivery_type):
            res = getattr(self, '%s_rate_shipment' % self.delivery_type)(order)
            # apply margin on computed price
            res['price'] = float(res['price']) * (1.0 + (self.margin / 100.0))
            # save the real price in case a free_over rule overide it to 0
            res['carrier_price'] = res['price']
            # free when order is large enough
            if res['success'] and self.free_over and order._compute_amount_total_without_delivery() >= self.amount:
                res['warning_message'] = _('The shipping is free since the order amount exceeds %.2f.') % (self.amount)
                res['price'] = 0.0
            return res    