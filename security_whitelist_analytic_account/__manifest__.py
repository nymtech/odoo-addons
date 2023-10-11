# -*- coding: utf-8 -*-

{
    "name": "Security Whitelist for analytic accounts",
    "category": "Security",
    "version": "14.0.1.0.0",
    "installable": True,
    "license": "AGPL-3",
    "author": "Gautier Casabona",
    "website": "https://www.open-net.ch",
    "depends": ["security_whitelist", "analytic"],
    "data": [
        # Data
        "data/function.xml",
        # Security
        "security/ir_rule.xml",
        # Views
        "views/account_analytic_account.xml",
    ],
}
