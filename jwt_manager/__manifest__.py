# -*- coding: utf-8 -*-

{
    'name': "JWT manager",
    'category': "Tools",
    'version': "14.0.1.0.0",
    'installable': True,
    'sequence': 1,

    'license': "AGPL-3",
    'author': "Gautier Casabona",
    'website': "https://www.open-net.ch",

    'depends': ['mail'],

    'data': [
        # Views
        'views/json_web_token.xml',

        # Menu items
        'data/menuitem.xml',

        # Security
        'security/security.xml',
        'security/ir.model.access.csv',
    ],

    "external_dependencies": {"python": ["cryptography", "pyjwt"]},

}
