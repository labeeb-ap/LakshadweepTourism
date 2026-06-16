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






    @http.route(
        '/api/water-sport/<int:water_sport_id>',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def water_sport_detail(self, water_sport_id, **kwargs):

        payload = verify_token()

        if not payload:
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Invalid or expired token'
                },
                status=401
            )

        water_sport = request.env[
            'tour.water.sport'
        ].sudo().search(
            [
                ('id', '=', water_sport_id),
                ('active', '=', True)
            ],
            limit=1
        )

        if not water_sport:
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Water Sport not found'
                },
                status=404
            )

        base_url = request.env[
            'ir.config_parameter'
        ].sudo().get_param(
            'web.base.url'
        )

        image_url = False

        if water_sport.image:
            image_url = (
                f"{base_url}/api/water-sport/image/{water_sport.id}"
            )
        print("haaaaaaaaaaaaaaaaaai")

        gallery_images = []

        for img in water_sport.image_ids:
            gallery_images.append({
                'id': img.id,
                'name': img.name or '',
                'image_url': (
                    f"{base_url}/api/water-sport/gallery/image/{img.id}"
                )
            })

        includes = []

        for include in water_sport.include_ids:
            includes.append({
                'id': include.id,
                'name': include.name
            })

        return request.make_json_response({
            'success': True,
            'message': 'Water Sport details fetched successfully',
            'data': {
                'id': water_sport.id,
                'name': water_sport.name,

                'island_id': water_sport.island_id.id,
                'island_code': water_sport.island_id.code,
                'island_name': water_sport.island_id.name,

                'image': image_url,
                'gallery_images': gallery_images,

                'price': water_sport.price,

                'duration': water_sport.duration or '',
                'age_limit': water_sport.age_limit or '',
                'group_size': water_sport.group_size or '',

                'description': water_sport.description or '',

                'includes': includes
            }
        })