from odoo import http
from odoo.http import request

from ..utils.jwt_helper import verify_token


class HomestayController(http.Controller):

    @http.route(
        '/api/homestays',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def homestays(self, **kwargs):

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

        homestays = request.env[
            'tour.homestay'
        ].sudo().search(domain)

        base_url = request.env[
            'ir.config_parameter'
        ].sudo().get_param(
            'web.base.url'
        )

        data = []

        for homestay in homestays:

            image_url = None

            if homestay.image:
                image_url = (
                    f"{base_url}/api/homestay/image/{homestay.id}"
                )

            data.append({
                'id': homestay.id,
                'name': homestay.name,
                'island_id': homestay.island_id.code,
                'island_name': homestay.island_id.name,
                'image': image_url,
                'rating': homestay.rating,
                'reviews': homestay.reviews,
                'price': homestay.price_per_night,
                'description': homestay.description or '',
            })

        return request.make_json_response({
            'success': True,
            'message': 'Homestays fetched successfully',
            'data': data
        })