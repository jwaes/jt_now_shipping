# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class ProviderNow(models.Model):
    _inherit = 'delivery.carrier'

    website_extra_info = fields.Boolean('website_extra_info', default=False)
    website_extra_info_html = fields.Html('website_extra_info_html')

    shipping_property_key_id = fields.Many2one('jt.property.key', string='Key')
    category_price_ids = fields.One2many('category.price', 'delivery_carrier_id', string='Category Price')

    not_free_price = fields.Float(string='Shipping cost', help="Price if we do not reach the minimum order price")

    delivery_type = fields.Selection(selection_add=[
        ('noweu', 'NOW EU')
    ], ondelete={'noweu': lambda recs: recs.write({'delivery_type': 'fixed', 'fixed_price': 0})})

    @api.onchange('shipping_property_key_id')
    def _onchange_key(self):
        for k in self:
            if k.shipping_property_key_id:
                for v in k.shipping_property_key_id.value_ids:
                    vid = v.id
                    vfound = False
                    for cp in k.category_price_ids:
                        if v.id == cp.id:
                            vfound=True
                            break
                    if not vfound:
                        self.env['category.price'].create({
                            'delivery_carrier_id': self.id.origin,
                            'property_value_id': v.id,
                        })

    def _get_price_for_category(self, category_code):
        for record in self:
            for category_price in record.category_price_ids:
                if category_price.code == category_code:
                    return category_price.price
        return False

    def noweu_rate_shipment(self, order):
        self.ensure_one()

        price = 0.0

        for line in order.order_line:
            _logger.info("Line %s", line)
            if line.is_delivery:
                _logger.info("is delivery ... skipping")
            else:
                product = line.product_id
                _logger.info("%s", product.name)
               
                code = self.shipping_property_key_id.code
                kvs = product.all_kvs.filtered(lambda kvi: kvi.code == code)
                if len(kvs) < 1:
                    _logger.error("Product %s : %s has no value set for %s", product, product.name, code)
                    return {'success': False,
                        'price': price,
                        'error_message': False,
                        'warning_message': "We could not calculate a shipping price"}
                if len(kvs) > 2:
                    _logger.error("Product %s : %s has multiple values set for %s :", product, product.name, code)
                    for kv in kvs:
                        _logger.error("- %s", kv.value_id.code)
                    return {'success': False,
                        'price': price,
                        'error_message': False,
                        'warning_message': "We could not calculate a shipping price"}
                shipping_categ_code = kvs[0].value_id.code                
                categ_price = self._get_price_for_category(shipping_categ_code)
                if categ_price is False:
                    return {'success': False,
                        'price': price,
                        'error_message': "We could not calculate a shipping price, please contact us.",
                        'warning_message': False}                    
                price += line.product_qty * categ_price
                _logger.info("+= %s * %s (%s) = %s", line.product_qty, categ_price, shipping_categ_code, price)

        total = order._compute_amount_total_without_delivery()
        if self.free_over and total < self.amount and price < self.not_free_price:
            price = self.not_free_price

        return {'success': True,
                'price': price,
                'error_message': False,
                'warning_message': "Warning"} 

class DeliveryCarrierCategoryPrice(models.Model):
    _name = 'category.price'
    _description = 'Delivery carrier category price'

    delivery_carrier_id = fields.Many2one('delivery.carrier', required=True, string='delivery_carrier')
    property_value_id = fields.Many2one('jt.property.value', required=True, string='Property Value')
    code = fields.Char(related='property_value_id.code')

    is_free = fields.Boolean('Free')

    price = fields.Float('Price', digits='Product Price')

    @api.onchange('is_free')
    def _onchange_is_free(self):
        for o in self:
            if o.is_free:
                o.price = 0.0
    