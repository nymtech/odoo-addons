from odoo import http
from odoo.http import request
from werkzeug.utils import redirect


def display_message(message):
    return """<html>
    <head>
        <title>Revolut authorization API</title>
    </head>
    <body>
        <h3>Error</h1>
        <div>{}</div>
    </body>""".format(message)


class RevolutController(http.Controller):

    @http.route('/revolut/authorize', type='http', auth='public')
    def authorize(self, **kwargs):
        code = kwargs.get('code')
        if not code:
            return display_message("No authorization code provided")
        if not request.env.company.revolut_jwt_id:
            return display_message("No revolut JWT set on company")

        res = request.env.company.revolut_jwt_id.get_revolut_access_token(code)

        if not res:
            return display_message("Couldn't get an access token, check server logs for Revolut API response")
        else:
            redirect(f'/web#id={request.env.company.revolut_jwt_id.id}&model=json.web.token&view_type=form')
