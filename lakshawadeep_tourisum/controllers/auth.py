import logging
import jwt

from datetime import datetime, timedelta, timezone

from odoo import http
from odoo.http import request


_logger = logging.getLogger(__name__)


class AuthController(http.Controller):

    @http.route(
        '/api/auth/signup',
        type='json',
        auth='public',
        methods=['POST'],
        csrf=False
    )
    def signup(self, **kwargs):

        name = kwargs.get('name')
        email = kwargs.get('email')
        phone = kwargs.get('phone')
        password = kwargs.get('password')

        if not name:
            return {
                'success': False,
                'message': 'Name is required'
            }

        if not email:
            return {
                'success': False,
                'message': 'Email is required'
            }

        if not phone:
            return {
                'success': False,
                'message': 'Phone is required'
            }

        if not password:
            return {
                'success': False,
                'message': 'Password is required'
            }

        existing_user = request.env['res.users'].sudo().search([
            ('login', '=', email)
        ], limit=1)

        if existing_user:
            return {
                'success': False,
                'message': 'Email already registered'
            }

        portal_group = request.env.ref('base.group_portal')

        user = request.env['res.users'].sudo().create({
            'name': name,
            'login': email,
            'email': email,
            'phone': phone,
            'password': password,
            'groups_id': [(6, 0, [portal_group.id])],
            'share': True,
        })

        user.partner_id.write({
            'is_customer': True
        })

        return {
            'success': True,
            'message': 'Registration successful',
            'data': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
            }
        }

    @http.route(
        '/api/auth/signin',
        type='json',
        auth='public',
        methods=['POST'],
        csrf=False
    )
    def signin(self, **kwargs):

        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email:
            return {
                'success': False,
                'message': 'Email is required'
            }

        if not password:
            return {
                'success': False,
                'message': 'Password is required'
            }

        try:
            auth_result = request.session.authenticate(
                request.db,
                {
                    'login': email,
                    'password': password,
                    'type': 'password'
                }
            )

            uid = auth_result.get('uid')

        except Exception as e:
            _logger.error("Authentication Error: %s", e)
            uid = False

        if not uid:
            return {
                'success': False,
                'message': 'Invalid email or password'
            }

        user = request.env['res.users'].sudo().browse(uid)

        # Read JWT settings from System Parameters
        config = request.env['ir.config_parameter'].sudo()

        jwt_secret = config.get_param('jwt.secret')
        jwt_algorithm = config.get_param(
            'jwt.algorithm',
            default='HS256'
        )
        jwt_expiry_days = int(
            config.get_param(
                'jwt.expiry_days',
                default='30'
            )
        )

        if not jwt_secret:
            return {
                'success': False,
                'message': 'JWT secret is not configured'
            }

        payload = {
            'uid': user.id,
            'email': user.email,
            'login': user.login,
            'exp': datetime.now(timezone.utc) + timedelta(
                days=jwt_expiry_days
            )
        }

        token = jwt.encode(
            payload,
            jwt_secret,
            algorithm=jwt_algorithm
        )

        response = {
            'success': True,
            'message': 'Login successful',
            'token': token,
            'data': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
            }
        }

        _logger.info("LOGIN RESPONSE: %s", response)

        return response

