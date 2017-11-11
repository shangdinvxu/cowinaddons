# -*- coding: utf-8 -*-
{
    'name': "cowin_settings",

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
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/menu_actions.xml',
        'views/sequences.xml',
        'views/cowin_setting_process.xml',
        'views/cowin_settings_process_stage.xml',
        'views/cowin_settings_process_tache.xml',
        'views/templates.xml',
        'views/views.xml',
        'views/init_custom_model.xml',
        'views/init_process.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
}