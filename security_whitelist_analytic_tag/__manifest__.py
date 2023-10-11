# -*- coding: utf-8 -*-

{
    "name": "Security whitelist for analytic tags",
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
        "views/account_analytic_tag.xml",
    ],
}
