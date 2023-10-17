from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
import requests
import re
import json
import logging
_logger = logging.getLogger(__name__)


DEFAULT_AUTHORIZED_ENDPOINTS = [
    '/auth/token',
    '/accounts',
    '/accounts/*/bank-details',
    '/transactions?*',
]


class JsonWebToken(models.Model):
    _inherit = "json.web.token"

    is_revolut = fields.Boolean(compute="_compute_is_revolut")
    revolut_access_token = fields.Char(string='Revolut Access Token')
    revolut_access_token_expiration = fields.Datetime(string='Revolut Access Token Expiration')
    revolut_refresh_token = fields.Char(string='Revolut Refresh Token', tracking=True)
    revolut_token_is_expired = fields.Boolean(compute="_compute_revolut_token_expired")

    show_revolut_help = fields.Boolean()
    authorized_endpoint_ids = fields.One2many('revolut.endpoint', 'jwt_id', string='Authorized Endpoints')


    @api.depends('revolut_access_token', 'revolut_refresh_token')
    def _compute_is_revolut(self):
        for token in self:
            token.is_revolut = token.payload_line_ids.filtered(lambda l: l.key == 'aud' and l.value == 'https://revolut.com').exists()

    @api.depends('revolut_access_token_expiration')
    def _compute_revolut_token_expired(self):
        for token in self:
            token.revolut_token_is_expired = token.revolut_access_token_expiration and token.revolut_access_token_expiration < fields.Datetime.now()


    # --------------------------------------------
    #                   Public
    # --------------------------------------------


    def get_revolut_api_url(self):
        return self.env['ir.config_parameter'].sudo().get_param('revolut.api.url')

    def ask_revolut_api(self, endpoint, payload=None):
        self.ensure_one()
        if self.revolut_access_token_expiration < fields.Datetime.now():
            if not self.refresh_revolut_access_token():
                raise UserError(_("Couldn't refresh access token, check server logs for Revolut API response"))
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.revolut_access_token}',
        }
        payload = payload or {}
        _logger.debug("Sending request to Revolut API: %s" % endpoint)
        return self._send_revolut_request(endpoint, headers=headers, data=payload)


    # --------------------------------------------
    #                   Private
    # --------------------------------------------


    def _check_endpoint_whitelist(self, endpoint):
        regex_str_list = [e._get_regex_str() for e in self.authorized_endpoint_ids]
        if not any(re.match(r, endpoint) for r in regex_str_list):
            raise UserError(_("Revolut API endpoint '%s' is not whitelisted\nPlease check '%s' settings", endpoint, self.name))

    def _send_revolut_request(self, endpoint, method="GET", headers=None, data=None):
        self._check_endpoint_whitelist(endpoint)
        url = self.get_revolut_api_url() + endpoint
        headers = headers or {}
        data = data or {}
        res = requests.request(method, url, headers=headers, data=data)
        if res.status_code != 200:
            raise UserError(_("Revolut API call returned a %s status code:\n\n %s" % (res.status_code, res.text)))
        return json.loads(res.text)

    def _update_revolut_token_infos(self, res, *args):
        if not all([k in res for k in args]):
            _logger.error("json.web.token: Missing infos while updating token, response from API: %s " % res)
            return False

        _logger.info("Updating Revolut token infos: %s" % ', '.join(args))
        infos = {}
        if 'access_token' in args:
            infos['revolut_access_token'] = res.get('access_token')
        if 'refresh_token' in args:
            infos['revolut_refresh_token'] = res.get('refresh_token')
        if 'expires_in' in args:
            infos['revolut_access_token_expiration'] = fields.Datetime.now() + relativedelta(seconds=res.get('expires_in') - 60)

        self.write(infos)
        return True






    # --------------------------------------------
    #          Non authenticated methods
    # --------------------------------------------


    def get_revolut_access_token(self, authorization_code):
        self.ensure_one()
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
            'client_assertion': self.jwt,
        }
        res = self._send_revolut_request("/auth/token", method="POST", headers=headers, data=data)
        return self._update_revolut_token_infos(res, 'access_token', 'refresh_token', 'expires_in')


    def refresh_revolut_access_token(self):
        self.ensure_one()
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.revolut_refresh_token,
            'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
            'client_assertion': self.jwt,
        }
        _logger.info("Refreshing Revolut access token")
        res = self._send_revolut_request("/auth/token", method="POST", headers=headers, data=data)
        return self._update_revolut_token_infos(res, 'access_token', 'expires_in')



    # --------------------------------------------
    #                 Actions
    # --------------------------------------------


    def action_reset_authorized_endpoints(self):
        self.ensure_one()
        self.authorized_endpoint_ids = [(5, 0, 0)] + [(0, 0, {'name': endpoint}) for endpoint in DEFAULT_AUTHORIZED_ENDPOINTS]
        return {}

    def action_toggle_help(self):
        self.ensure_one()
        self.show_revolut_help = not self.show_revolut_help
        return {}

