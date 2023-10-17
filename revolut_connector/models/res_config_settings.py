from odoo import fields, models
from dateutil.relativedelta import relativedelta


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    revolut_jwt_id = fields.Many2one(related='company_id.revolut_jwt_id', readonly=False)


    def action_synchronize_revolut_accounts(self):
        self.env['res.partner.bank'].synchronize_revolut_accounts()


    def action_open_revolut_generate_jwt_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Generate JWT',
            'res_model': 'revolut.generate.jwt.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_company_id': self.env.company.id,
                'default_expiration_date': fields.Datetime.now() + relativedelta(years=10),
            },
        }
