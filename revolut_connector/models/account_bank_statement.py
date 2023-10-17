from odoo import fields, models


class AccountBankStatement(models.Model):
    _inherit = "account.bank.statement"

    revolut_id = fields.Char(string='Revolut ID', index=True)

