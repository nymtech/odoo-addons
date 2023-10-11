from odoo import models


class AccountAnalyticAccount(models.Model):
    _name = "account.analytic.account"
    _inherit = ["account.analytic.account", "whitelist.mixin"]

    def _get_allowed_group_ids(self):
        return ['analytic.group_analytic_accounting']
