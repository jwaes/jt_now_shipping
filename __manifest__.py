# -*- coding: utf-8 -*-
{
    'name': "jt_now_shipping",

    'summary': "JT NOW shipping cost calculation",

    'description': "",

    'author': "jaco tech",
    'website': "https://jaco.tech",
    "license": "AGPL-3",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.11',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'delivery',
        'website_sale_delivery',
        'jt_product_properties',
    ],

    # always loaded
    'data': [
        'data/jt_now_shipping_data.xml',
        'security/ir.model.access.csv',
        'views/delivery_view.xml',
        'views/website_sale_delivery_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
