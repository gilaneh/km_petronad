# -*- coding: utf-8 -*-
{
    'name': "km_petronad",

    'summary': """
        """,

    'description': """
        
    """,

    'author': "Arash Homayounfar",
    'website': "https://gilaneh.com/",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Service Desk/Service Desk',
    'application': True,
    'version': '1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'mail', 'project', 'sd_apps', 'hr'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/dashboard.xml',
        'views/feeds.xml',
        'views/sale.xml',
        'views/production.xml',
        'views/views.xml',
        'wizard/report_wizard.xml',
        'wizard/data_input_wizard.xml',
        'wizard/data_view_wizard.xml',
        'views/petronad.xml',
        'report/daily_report.xml',
        'report/daily_report_template.xml',
        ],
    'assets': {
        'web._assets_common_scripts': [
        ],
        'web._assets_common_styles': [
            'km_petronad/static/src/css/report.css',
        ],
        'web.assets_backend': [
            # 'km_petronad/static/src/lib/plotlyjs_2.27.1/plotly.min.js',
            # 'km_petronad/static/src/js/plotly.min.js',
            'km_petronad/static/src/js/km_petronad_data_view.js',
            # 'km_petronad/static/src/js/plotly_field.js',

        ],
        'web.assets_frontend': [

],
        'web.report_assets_common': [
            'km_petronad/static/src/css/report.css',

        ],
        },
    'license': 'LGPL-3',
}