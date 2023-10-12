from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class JsonWebTokenPayloadLine(models.Model):
    _name = "json.web.token.payload.line"
    _description = "json.web.token.payload.line"

    json_web_token_id = fields.Many2one('json.web.token', string='Json Web Token', required=True, ondelete='cascade')
    key = fields.Char(string='Key', required=True)
    value = fields.Char(string='Value', required=True)
    type = fields.Selection(
        selection=[
            ('string', 'String'),
            ('integer', 'Integer'),
            ('float', 'Float'),
        ],
        string='Force Type',
        default='string',
        required=True,
    )

    def get_typed_value(self):
        self.ensure_one()
        if self.type == 'integer':
            return int(self.value)
        elif self.type == 'float':
            return float(self.value)
        else:
            return self.value

    @api.constrains('value', 'type')
    def _check_type(self):
        for line in self:
            try:
                if line.type == 'integer':
                    int(line.value)
                elif line.type == 'float':
                    float(line.value)

            except ValueError:
                raise ValidationError(_("'%s' can't be cast as %s", line.value, line.type))

