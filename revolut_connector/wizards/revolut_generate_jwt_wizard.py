from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)

class RevolutGenerateJwtWizard(models.TransientModel):
    _name = "revolut.generate.jwt.wizard"
    _description = "revolut.generate.jwt.wizard"

    company_id = fields.Many2one('res.company', string='Company', required=True)
    private_key_path = fields.Char(string='Private Key Path', required=True)
    public_key_path = fields.Char(string='Public Key Path', required=True)
    client_id = fields.Char(string='Client ID', required=True)
    expiration_date = fields.Date(string='Expiration Date', required=True)
    issuer = fields.Char(string='Issuer', required=True)

    authorization_url = fields.Char(string='Authorization URL', compute="_compute_authorization_url")


    @api.depends('company_id')
    def _compute_authorization_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if base_url[-1] != '/':
            base_url += '/'
        for wizard in self:
            wizard.authorization_url = base_url + 'revolut/authorize'

    def generate_jwt_record(self):
        self.ensure_one()
        revolut_jwt_id = self.env['json.web.token'].create({
            'name': 'Revolut API connector for %s' % self.company_id.name,
            'private_key_path': self.private_key_path,
            'public_key_path': self.public_key_path,
            'expiration_date': self.expiration_date,
            'algorithm': 'RS256',
            'payload_line_ids': [
                (0, 0, {'key': 'aud', 'value': 'https://revolut.com'}),
                (0, 0, {'key': 'sub', 'value': self.client_id}),
                (0, 0, {'key': 'iss', 'value': self.issuer}),
            ],
        })
        self.company_id.revolut_jwt_id = revolut_jwt_id.id
        try:
            revolut_jwt_id.generate_jwt()
        except Exception as e:
            _logger.error("Couldn't generate JWT: %s" % e)
        revolut_jwt_id.action_reset_authorized_endpoints()
        return revolut_jwt_id.get_formview_action()

