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



            data.append({
                'id': restaurant.id,
                'name': restaurant.name,
                'island_id': restaurant.island_id.code,
                'island_name': restaurant.island_id.name,
                'image': image_url,
                'description': restaurant.description or '',
            })

        return request.make_json_response({
            'success': True,
            'message': 'Restaurants fetched successfully',
            'data': data
        })

from odoo import http
from odoo.http import request

from ..utils.jwt_helper import verify_token

class RestaurantController(http.Controller):

    @http.route(
        '/api/restaurant/<int:restaurant_id>',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def restaurant_detail(self, restaurant_id, **kwargs):

        payload = verify_token()

        if not payload:
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Invalid or expired token'
                },
                status=401
            )

        restaurant = request.env[
            'tour.restaurant'
        ].sudo().search(
            [
                ('id', '=', restaurant_id),
                ('active', '=', True)
            ],
            limit=1
        )

        if not restaurant:
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Restaurant not found'
                },
                status=404
            )

        base_url = request.env[
            'ir.config_parameter'
        ].sudo().get_param(
            'web.base.url'
        )

        image_url = False

        if restaurant.image:
            image_url = (
                f"{base_url}/api/restaurant/image/{restaurant.id}"
            )

        cuisines = []

        for cuisine in restaurant.cuisine_ids:
            cuisines.append({
                'id': cuisine.id,
                'name': cuisine.name
            })

        opening_time = ''

        if restaurant.opening_time:
            opening_time = (
                f"{restaurant.opening_time} "
                f"{(restaurant.opening_period or '').upper()}"
            )

        closing_time = ''

        if restaurant.closing_time:
            closing_time = (
                f"{restaurant.closing_time} "
                f"{(restaurant.closing_period or '').upper()}"
            )

        return request.make_json_response({
            'success': True,
            'message': 'Restaurant details fetched successfully',
            'data': {
                'id': restaurant.id,
                'name': restaurant.name,

                'island_id': restaurant.island_id.id,
                'island_code': restaurant.island_id.code,
                'island_name': restaurant.island_id.name,

                'image': image_url,

                'description': restaurant.description or '',

                'phone': restaurant.phone or '',

                'opening_time': opening_time,
                'closing_time': closing_time,

                'opening_note': restaurant.opening_note or '',

                'address': restaurant.address or '',

                'latitude': restaurant.latitude or 0.0,
                'longitude': restaurant.longitude or 0.0,

                'cuisines': cuisines
            }
        })