![Stars](https://img.shields.io/github/stars/nymtech/odoo-addons?style=social)
![Watchers](https://img.shields.io/github/watchers/nymtech/odoo-addons?style=social)
![Forks](https://img.shields.io/github/forks/nymtech/odoo-addons?style=social)

![LastCommit](https://img.shields.io/github/last-commit/nymtech/odoo-addons?color=green)

# Security Whitelist Bundle Version 14.0

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

| Addons                                                                     | Description                                                                                      | Installation         | Dependencies            |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | -------------------- | ----------------------- |
| [jwt_manager](jwt_manager/)                                                | Allow users to generate Json Web Token from Odoo<br/>Mainly used as a depends for others modules | Apps library         | mail                    |
| [revolut_connector](revolut_connector)                                     | A Revolut connector that allows you to mass import transactions into bank statements<br/>        | Apps library         | account<br/>jwt_manager |
| [security_whitelist](security_whitelist)                                   | Main module<br/>It does nothing by itself, you can activate its features in the module settings  | Apps library         |                         |
| [security_whitelist_account_budget](security_whitelist_account_budget)     | Manage users accesses on accounting budgets                                                      | Main module settings |                         |
| [security_whitelist_account_journal](security_whitelist_account_journal)   | Manage users accesses on accounting journals                                                     | Main module settings |                         |
| [security_whitelist_analytic_account](security_whitelist_analytic_account) | Manage users accesses on analytic accounts                                                       | Main module settings |                         |
| [security_whitelist_analytic_tag](security_whitelist_analytic_tag)         | Manage users accesses on analytic tags                                                           | Main module settings |                         |
