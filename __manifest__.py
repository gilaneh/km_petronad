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
    'version': '1.1.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'mail', 'project', 'hr'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/dashboard.xml',
        'views/feeds.xml',
        'views/shutdown.xml',
        'views/sale.xml',
        'views/production.xml',
        'views/storage.xml',
        'views/tanks.xml',
        'views/views.xml',
        # 'wizard/report_wizard.xml',
        # 'wizard/data_input_wizard.xml',
        # 'wizard/data_view_wizard.xml',
        'views/comments.xml',
        'views/petronad.xml',
        'data/product_type_data.xml',
        'data/shutdown_type_data.xml',
        # 'report/daily_report.xml',
        # 'report/daily_report_template.xml',
        ],
    'assets': {
        'web._assets_common_scripts': [
        ],
        'web._assets_common_styles': [
            'km_petronad/static/src/css/report.css',
        ],
        'web.assets_qweb': [
            'km_petronad/static/src/components/**/*.xml',
        ],
        'web.assets_backend': [
            # 'km_petronad/static/src/lib/plotlyjs_2.27.1/plotly.min.js',
            # 'km_petronad/static/src/js/plotly.min.js',
            # 'km_petronad/static/src/js/km_petronad_data_view.js',
            'km_petronad/static/src/components/**/*.js',
            'km_petronad/static/src/components/**/*.scss',

        ],
        'web.assets_frontend': [

],
        'web.report_assets_common': [
            'km_petronad/static/src/css/report.css',

        ],
        },
    'license': 'LGPL-3',
}
