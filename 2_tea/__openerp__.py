# -*- coding: utf-8 -*-
{
    'name': "2Tea",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web_one2many_kanban', 'web_responsive', 'web_tree_image'],

    # always loaded
    'data': [
        'security/user_security.xml',
        'security/ir.model.access.csv',
        # 'security/ir.model.access.csv',
        'views/food_view.xml',
        'views/km_view.xml',
        'views/ban_view.xml',
        'views/order_view.xml',
        'views/order_mon_view.xml',
        'views/templates.xml',
        'menu/menu.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
         'demo/demo.xml',
         'demo/ban_status_data.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}