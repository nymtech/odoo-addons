from odoo import models


class AccountAnalyticTag(models.Model):
    _name = "account.analytic.tag"
    _inherit = ["account.analytic.tag", "whitelist.mixin"]

    def _get_allowed_group_ids(self):
        return ["analytic.group_analytic_tags"]
