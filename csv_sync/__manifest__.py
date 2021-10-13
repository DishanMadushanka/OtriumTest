# -*- coding: utf-8 -*-
{

    'name': 'CSV Sync',

    'version': '12.0',

    'summary': 'Data Sync Process In Device and Content',

    'description': "Otrium Test",

    'category': '',

    'author': 'Dishan Madushanka',

    'website': '',

    'depends': [
        'base',
    ],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'view/content_view.xml',
        'view/device_view.xml',
        # 'view/settings_form.xml',
        'wizard/csv_content_import_view.xml',
        'wizard/csv_device_import_view.xml',
    ],

    'images': [],

    'license': '',

    'installable': True,

    'application': True,

    'auto_install': False,
}
