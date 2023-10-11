from odoo import models


class CrossoveredBudget(models.Model):
    _name = "crossovered.budget"
    _inherit = ["crossovered.budget", "whitelist.mixin"]

    def _get_allowed_group_ids(self):
        return ['account.group_account_manager']
