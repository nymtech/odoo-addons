from odoo import fields, models, _
from odoo.exceptions import UserError
from datetime import datetime
import subprocess
import jwt
from pathlib import Path
import logging
_logger = logging.getLogger(__name__)

class JsonWebToken(models.Model):
    _name = "json.web.token"
    _description = "json.web.token"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    jwt = fields.Char(string='JWT', readonly=True)

    private_key_path = fields.Char(string='Private Key Path', required=True)
    public_key_path = fields.Char(string='Public Key Path', required=True)
    expiration_date = fields.Date()
    algorithm = fields.Selection(
        selection=[
            # ('HS256', 'HS256'),
            ('RS256', 'RS256'),
        ],
        string='Signing Algorithm',
        required=True,
    )
    payload_line_ids = fields.One2many('json.web.token.payload.line', 'json_web_token_id', string='Payload Values')


    def _generate_payload(self):
        self.ensure_one()
        return {line.key: line.get_typed_value() for line in self.payload_line_ids}

    def generate_jwt(self):
        self.ensure_one()
        if not self.payload_line_ids:
            raise UserError(_('Please add payload values'))

        private_key_path = Path(self.private_key_path).resolve()
        if not private_key_path.exists():
            raise UserError(_('Private key path does not exist: %s' % private_key_path))

        private_key = subprocess.check_output(['cat', private_key_path])

        payload = self._generate_payload()
        payload['exp'] = int(datetime.timestamp(fields.Datetime.to_datetime(self.expiration_date)))

        self.jwt = jwt.encode(payload, private_key, algorithm=self.algorithm)


