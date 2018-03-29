# -*- coding: utf-8 -*-
{
    'name': "cowin_foundation",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'cowin_hr', 'cowin_plugin'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/templates.xml',
        'views/cowin_foundation.xml',
        'views/cowin_foundation_GP.xml',
        'views/cowin_foundation_intermediary_info.xml',
        'views/cowin_foundation_management_company.xml',
        'views/cowin_foundation_sponsor.xml',
        # 'demo/demo.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'qweb': ['static/src/xml/*.xml'],
}