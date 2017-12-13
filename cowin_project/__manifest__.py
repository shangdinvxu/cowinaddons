# -*- coding: utf-8 -*-
{
    'name': "cowin_project",

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
    'depends': ['base', 'cowin_hr', 'cowin_foundation','cowin_common', 'cowin_settings'],

    # always loaded
    'data': [

        'security/project_security.xml',
        'security/ir.model.access.csv',
        'security/dependencies_many2many/ir.model.access.csv',
        'security/settings/ir.model.access.csv',
        'security/settings/approval_settings/ir.model.access.csv',
        'security/sub_project/ir.model.access.csv',
        'security/sub_project/prev_investment_management/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/sub_project/prev_investment_management/*.xml',
        'views/dependencies_many2many/sub_project_round_financing_and_foundation.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
}