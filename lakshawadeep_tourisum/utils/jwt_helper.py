import jwt

from odoo.http import request


def verify_token():

    auth_header = request.httprequest.headers.get('Authorization')

    if not auth_header:
        print('No Authorization header')
        return False

    try:
        token = auth_header.replace('Bearer ', '')

        config = request.env['ir.config_parameter'].sudo()

        jwt_secret = config.get_param('jwt.secret')
        jwt_algorithm = config.get_param(
            'jwt.algorithm',
            default='HS256'
        )

        payload = jwt.decode(
            token,
            jwt_secret,
            algorithms=[jwt_algorithm]
        )

        return payload

    except Exception:
        return False