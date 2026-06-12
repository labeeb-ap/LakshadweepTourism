from odoo import http
from odoo.http import request

from ..utils.jwt_helper import verify_token


class TaxiController(http.Controller):

    @http.route(
        '/api/taxis',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def taxis(self, **kwargs):

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

        taxis = request.env[
            'tour.taxi'
        ].sudo().search(domain)

        base_url = request.env[
            'ir.config_parameter'
        ].sudo().get_param(
            'web.base.url'
        )

        data = []

        for taxi in taxis:

            image_url = None

            if taxi.image:
                image_url = (
                    f"{base_url}/api/taxi/image/{taxi.id}"
                )

            data.append({
                'id': taxi.id,
                'name': taxi.name,
                'island_id': taxi.island_id.code,
                'island_name': taxi.island_id.name,
                'image': image_url,
                'vehicle_type': taxi.vehicle_type,
                'seater': taxi.seater,
                'ac': taxi.ac,
                'description': taxi.description or '',
            })

        return request.make_json_response({
            'success': True,
            'message': 'Taxi services fetched successfully',
            'data': data
        })