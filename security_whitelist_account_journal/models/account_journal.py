from odoo import models


class AccountJournal(models.Model):
    _name = "account.journal"
    _inherit = ["account.journal", "whitelist.mixin"]

    def _get_allowed_group_ids(self):
        return ['account.group_account_manager']
