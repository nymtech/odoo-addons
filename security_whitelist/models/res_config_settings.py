from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_security_whitelist_account_journal = fields.Boolean()
    module_security_whitelist_analytic_account = fields.Boolean()
    module_security_whitelist_analytic_tag = fields.Boolean()
    module_security_whitelist_account_budget = fields.Boolean()

    # Todo: add a list of installed module to filter in the view
