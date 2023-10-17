from odoo import api, fields, models


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    revolut_id = fields.Char(string='Revolut ID', readonly=True)


    @api.model
    def synchronize_revolut_accounts(self):
        bank_accounts = self.search([('bank_id.bic', '=like', 'REVOGB%')])
        jwt_to_revolut_infos = {}

        for account in bank_accounts:
            revolut_jwt_id = account.company_id.revolut_jwt_id
            if not revolut_jwt_id or revolut_jwt_id in jwt_to_revolut_infos:
                continue

            jwt_to_revolut_infos[revolut_jwt_id] = revolut_jwt_id.ask_revolut_api('/accounts')
            for revolut_account in jwt_to_revolut_infos[revolut_jwt_id]:
                # Account is already 'linked'
                if bank_accounts.filtered(lambda a: a.revolut_id == revolut_account['id']):
                    continue

                revolut_account_details = revolut_jwt_id.ask_revolut_api('/accounts/%s/bank-details' % revolut_account['id'])
                if revolut_account_details:
                    valid_bank_account = None
                    for account_detail in revolut_account_details:
                        if 'iban' in account_detail:
                            valid_bank_account = account_detail
                            break

                    if valid_bank_account:
                        bank_accounts.filtered(lambda a: a.sanitized_acc_number == valid_bank_account['iban'] and a.currency_id.name == revolut_account.get('currency')).write({
                            'revolut_id': revolut_account['id'],
                        })


