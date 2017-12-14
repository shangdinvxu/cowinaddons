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

        #  prev_investment_management
        'views/sub_project/prev_investment_management/sub_project_application_form_for_project_investment.xml',
        'views/sub_project/prev_investment_management/sub_project_appointment_and_dismissal.xml',
        'views/sub_project/prev_investment_management/sub_project_call_up_record.xml',
        'views/sub_project/prev_investment_management/sub_project_conference_resolutions.xml',
        'views/sub_project/prev_investment_management/sub_project_dispatch_report.xml',
        'views/sub_project/prev_investment_management/sub_project_establishment.xml',
        'views/sub_project/prev_investment_management/sub_project_investment_contract.xml',
        'views/sub_project/prev_investment_management/sub_project_investment_decision_application.xml',
        'views/sub_project/prev_investment_management/sub_project_investment_decision_committee_meeting_resolution.xml',
        'views/sub_project/prev_investment_management/sub_project_opinion_book.xml',
        'views/sub_project/prev_investment_management/sub_project_payment_application_form.xml',
        'views/sub_project/prev_investment_management/sub_project_project_data_archiving.xml',
        'views/sub_project/prev_investment_management/sub_project_project_entrusted_loan_application_form.xml',
        'views/sub_project/prev_investment_management/sub_project_sum_investment_decision_committee.xml',


        # post_investment_management



        'views/dependencies_many2many/sub_project_round_financing_and_foundation.xml',

        'report/setup_project.xml',
        'report/common_report.xml',
        'report/register_information.xml',
        'report/project_setup_opinion.xml',
        'report/search_visit_record.xml',
        'report/invest_decision.xml',
        'report/invest_decison_resolution.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
}