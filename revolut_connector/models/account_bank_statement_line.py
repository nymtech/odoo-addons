from odoo import fields, models


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    revolut_id = fields.Char(string='Revolut ID', index=True)
