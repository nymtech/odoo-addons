from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    revolut_jwt_id = fields.Many2one('json.web.token', string='Revolut JWT')
