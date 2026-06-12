from odoo import http
from odoo.http import request

from ..utils.jwt_helper import verify_token


class WaterSportController(http.Controller):

    @http.route(
        '/api/water-sports',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def water_sports(self, **kwargs):

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

        sports = request.env[
            'tour.water.sport'
        ].sudo().search(domain)

        base_url = request.env[
            'ir.config_parameter'
        ].sudo().get_param(
            'web.base.url'
        )

        data = []

        for sport in sports:

            image_url = None

            if sport.image:
                image_url = (
                    f"{base_url}/api/water-sport/image/{sport.id}"
                )

            data.append({
                'id': sport.id,
                'name': sport.name,
                'island_id': sport.island_id.code,
                'island_name': sport.island_id.name,
                'image': image_url,
                'price': sport.price,
                'description': sport.description or '',
            })

        return request.make_json_response({
            'success': True,
            'message': 'Water sports fetched successfully',
            'data': data
        })