# -*- coding: utf-8 -*-
{
    'name': "cowin_hr",

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
    'depends': ['base',
                'hr',
                'cowin_common',
                ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/init_global_spec_appro_role_or_group_role.xml',
        'views/initadmin_relation_employee.xml',
        'views/init_hr_kanpan_for_different_user.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/sequences.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
}