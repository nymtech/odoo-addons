# -*- coding: utf-8 -*-

{
    "name": "Security Whitelist for account budgets",
    "category": "Security",
    "version": "14.0.1.0.0",
    "installable": True,
    "sequence": 1,
    "license": "AGPL-3",
    "author": "Gautier Casabona",
    "website": "https://www.open-net.ch",
    "depends": ["security_whitelist", "account_budget"],
    "data": [
        # Data
        "data/function.xml",
        # Security
        "security/ir_rule.xml",
        # Views
        "views/crossovered_budget.xml",
    ],
}
