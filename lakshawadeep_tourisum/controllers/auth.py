from odoo import http
from odoo.http import request


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
            'message': 'Registration successful1',
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

        except Exception:
            uid = False

        if not uid:
            return {
                'success': False,
                'message': 'Invalid email or password'
            }

        user = request.env['res.users'].sudo().browse(uid)

        return {
            'success': True,
            'message': 'Login successful',
            'data': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
            }
        }
