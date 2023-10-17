from odoo import fields, models
import urllib.parse
import logging
_logger = logging.getLogger(__name__)

class AccountJournal(models.Model):
    _inherit = "account.journal"

    revolut_id = fields.Char(related='bank_account_id.revolut_id')
    revolut_jwt_id = fields.Many2one(related='company_id.revolut_jwt_id')

    def import_revolut_statements(self, date_from, date_to, group_by):
        date_from = date_from.strftime('%Y-%m-%d') if date_from else False
        date_to = min(date_to, fields.Date.today()).strftime('%Y-%m-%d') if date_to else False
        revolut_jwt_id = self.sudo().revolut_jwt_id

        for journal in self.filtered('revolut_id'):
            params = {
                'account': journal.revolut_id,
            }
            # Todo: add a one day buffer to date_from and date_to
            if date_from:
                params['from'] = date_from
            if date_to:
                params['to'] = date_to

            res = revolut_jwt_id.ask_revolut_api("/transactions?%s" % urllib.parse.urlencode(params))

            statement_date = False
            starting_balance = False
            lines_vals_list = []

            for statement in res:
                # Todo: filter by completed_at date
                if statement.get('state') not in ['completed']:
                    continue

                # Todo: update if exists
                if self.env['account.bank.statement.line'].search([('revolut_id', '=', statement.get('id'))]):
                    continue

                transaction = None
                for t in statement.get('legs'):
                    if t.get('currency') != journal.currency_id.name:
                        continue
                    transaction = t
                if not transaction:
                    continue


                # Receive few infos from the transactions for bank statement
                starting_balance = transaction['balance'] - transaction['amount']
                if not statement_date:
                    statement_date = statement.get('created_at').split('T')[0]

                line_vals = {
                    'revolut_id': statement.get('id'),
                    'date': statement.get('created_at').split('T')[0],
                    'payment_ref': transaction.get('description'),
                    'amount': transaction['amount'],
                }
                if 'merchant' in statement:
                    partner = self.env['res.partner'].search([('name', 'ilike', statement.get('merchant', {}).get('name', ''))], limit=1)
                    if partner:
                        line_vals['partner_id'] = partner.id

                if 'bill_amount' in transaction:
                    line_vals['amount_currency'] = transaction['bill_amount']
                if 'bill_currency' in transaction:
                    line_vals['foreign_currency_id'] = self.env['res.currency'].with_context(active_test=False).search([('name', '=', transaction.get('bill_currency'))], limit=1).id


                lines_vals_list.append((0, 0, line_vals))


            if lines_vals_list:
                vals = {
                    'journal_id': journal.id,
                    'date': statement_date,
                    'line_ids': lines_vals_list,
                    'balance_start': starting_balance,
                }
                self.env['account.bank.statement'].create(vals)



