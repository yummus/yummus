# -*- coding: utf-8 -*-
{
    'name': "amazon_logs_added",

    'summary': """
        Add logs for amazon""",

    'description': """
        Add logs for amazon
    """,

    'author': "Odoo Yla",
    'website': "",
    'license': 'LGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_amazon_spapi','sale_amazon'],

    # always loaded
    'data': [],
    # only loaded in demonstration mode
    'demo': [],
}

