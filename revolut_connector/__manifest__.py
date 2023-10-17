# -*- coding: utf-8 -*-

{
    'name': "Revolut connector for Odoo",
    'category': "Accounting",
    'version': "14.0.1.0.0",
    'installable': True,
    'sequence': 1,

    'license': "AGPL-3",
    'author': "Gautier Casabona",
    'website': "https://www.open-net.ch",

    'depends': [
        'account',
        'jwt_manager',
    ],

    'data': [
        # Data
        'data/ir_config_parameter.xml',

        # Security
        'security/ir.model.access.csv',

        # Views
        'views/json_web_token.xml',
        'views/res_config_settings.xml',
        'views/res_company.xml',
        'views/res_partner_bank.xml',

        # Wizards
        'wizards/revolut_generate_jwt_wizard.xml',
        'wizards/revolut_import_statement_wizard.xml',

        # Menu items
        'data/menuitem.xml',
    ],
}
