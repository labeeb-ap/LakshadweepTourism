from odoo import http
from odoo.http import request

from ..utils.jwt_helper import verify_token


class ResortController(http.Controller):

    @http.route(
        '/api/resorts',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def resorts(self, **kwargs):

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
        print(island_code,"HAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

        domain = [('active', '=', True)]

        if island_code:

            island = request.env[
                'tour.island'
            ].sudo().search(
                [('code', '=', int(island_code))],
                limit=1
            )
            print(island.name,"BYYYYY")

            if island:
                domain.append(
                    ('island_id', '=', island.id)
                )
            else:
                return request.make_json_response({
                    'success': True,
                    'data': []
                })

        resorts = request.env[
            'tour.resort'
        ].sudo().search(domain)

        base_url = request.env[
            'ir.config_parameter'
        ].sudo().get_param(
            'web.base.url'
        )

        data = []

        for resort in resorts:

            image_url = None

            if resort.image:
                image_url = (
                    f"{base_url}/api/resort/image/{resort.id}"
                )

            data.append({
                'id': resort.id,
                'name': resort.name,
                'island_id': resort.island_id.code,
                'island_name': resort.island_id.name,
                'image': image_url,
                'price': resort.price_per_night,
                'description': resort.description or '',
                'room_count': resort.room_count,
            })

        return request.make_json_response({
            'success': True,
            'message': 'Resorts fetched successfully',
            'data': data
        })