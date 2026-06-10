from odoo import http
from odoo.http import request

from ..utils.jwt_helper import verify_token


class HomeController(http.Controller):

    @http.route(
        '/api/home',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def home(self, **kwargs):

        payload = verify_token()

        if not payload:
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Invalid or expired token'
                },
                status=401
            )

        islands = request.env['tour.island'].sudo().search(
            [('active', '=', True)],
            order='code'
        )

        base_url = request.env['ir.config_parameter'].sudo().get_param(
            'web.base.url'
        )

        island_data = []

        for island in islands:

            image_url = None

            if island.image:
                image_url = (
                    f"{base_url}/api/island/image/{island.id}"
                )

            island_data.append({
                'id': island.code,
                'name': island.name,
                'image': image_url,
                'description': island.description or '',
            })

        response = {
            'success': True,
            'message': 'Home data fetched successfully',
            'data': {
                'islands': island_data
            }
        }

        print("\n========== HOME API RESPONSE ==========")
        print(response)
        print("=======================================\n")

        return request.make_json_response(response)
