from odoo import fields, models


class RevolutImportStatementWizard(models.TransientModel):
    _name = "revolut.import.statement.wizard"
    _description = "revolut.import.statement.wizard"


    journal_ids = fields.Many2many(
        'account.journal',
        string='Journals',
        required=True,
        domain=[('bank_account_id.revolut_id', '!=', False)],
    )
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date')
    group_by = fields.Selection(
        selection=[
            ('day', 'Day'),
            ('week', 'Week'),
            ('month', 'Month'),
        ],
        string='Group by',
        default='day',
        required=True,
    )


    def import_statements(self):
        self.journal_ids.import_revolut_statements(
            date_from=self.date_from,
            date_to=self.date_to,
            group_by=self.group_by,
        )


