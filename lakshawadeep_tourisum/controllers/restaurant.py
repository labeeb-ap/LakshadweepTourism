from odoo import http
from odoo.http import request

from ..utils.jwt_helper import verify_token


class RestaurantController(http.Controller):

    @http.route(
        '/api/restaurants',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def restaurants(self, **kwargs):

        payload = verify_token()

        if not payload:
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Invalid or expired token'
                },
                status=401
            )

        island_code = kwargs.get('island')

        domain = [('active', '=', True)]

        if island_code:

            island = request.env[
                'tour.island'
            ].sudo().search(
                [('code', '=', int(island_code))],
                limit=1
            )

            if island:
                domain.append(
                    ('island_id', '=', island.id)
                )

        restaurants = request.env[
            'tour.restaurant'
        ].sudo().search(domain)

        base_url = request.env[
            'ir.config_parameter'
        ].sudo().get_param(
            'web.base.url'
        )

        data = []

        for restaurant in restaurants:

            image_url = None

            if restaurant.image:
                image_url = (
                    f"{base_url}/api/restaurant/image/{restaurant.id}"
                )

            cuisines = ", ".join(
                restaurant.cuisine_ids.mapped('name')
            )

            data.append({
                'id': restaurant.id,
                'name': restaurant.name,
                'island_id': restaurant.island_id.code,
                'island_name': restaurant.island_id.name,
                'image': image_url,
                'rating': restaurant.rating,
                'reviews': restaurant.reviews,
                'cuisines': cuisines,
                'description': restaurant.description or '',
            })

        return request.make_json_response({
            'success': True,
            'message': 'Restaurants fetched successfully',
            'data': data
        })