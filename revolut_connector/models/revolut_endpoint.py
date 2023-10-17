from odoo import fields, models
import re


class RevolutEndpoint(models.Model):
    _name = "revolut.endpoint"
    _description = "revolut.endpoint"

    name = fields.Char(required=True)
    jwt_id = fields.Many2one('json.web.token', string='JWT', required=True, ondelete='cascade')

    def _get_regex_str(self):
        self.ensure_one()
        return '^' + '.*'.join(list(map(re.escape, self.name.split('*')))) + '$'
