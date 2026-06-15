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
        print(island_code, "HAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

        domain = [('active', '=', True)]

        if island_code:

            island = request.env[
                'tour.island'
            ].sudo().search(
                [('code', '=', int(island_code))],
                limit=1
            )
            print(island.name, "BYYYYY")

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












    @http.route(
        '/api/resort/<int:resort_id>',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def resort_detail(self, resort_id, **kwargs):

        payload = verify_token()

        if not payload:
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Invalid or expired token'
                },
                status=401
            )

        resort = request.env['tour.resort'].sudo().search(
            [
                ('id', '=', resort_id),
                ('active', '=', True)
            ],
            limit=1
        )

        if not resort:
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Resort not found'
                },
                status=404
            )

        base_url = request.env[
            'ir.config_parameter'
        ].sudo().get_param(
            'web.base.url'
        )

        # Main Image
        image_url = False

        if resort.image:
            image_url = (
                f"{base_url}/api/resort/image/{resort.id}"
            )

        # Gallery Images
        gallery_images = []

        for img in resort.image_ids:
            gallery_images.append({
                'id': img.id,
                'name': img.name or '',
                'image_url': (
                    f"{base_url}/api/resort/gallery/image/{img.id}"
                )
            })

        return request.make_json_response({
            'success': True,
            'message': 'Resort details fetched successfully',
            'data': {
                'id': resort.id,
                'name': resort.name,
                'island_id': resort.island_id.id,
                'island_code': resort.island_id.code,
                'island_name': resort.island_id.name,

                # Main image
                'image': image_url,

                # Gallery images
                'gallery_images': gallery_images,

                'description': resort.description or '',
                'room_count': resort.room_count,
                'price_per_night': resort.price_per_night,
                'checkin_time': resort.checkin_time,
                'checkout_time': resort.checkout_time,

                'amenities': {
                    'sea_view': resort.sea_view,
                    'beach_access': resort.beach_access,
                    'free_wifi': resort.free_wifi,
                    'air_conditioning': resort.air_conditioning,
                    'restaurant': resort.restaurant,
                    'swimming_pool': resort.swimming_pool,
                    'free_breakfast': resort.free_breakfast,
                    'airport_transfer': resort.airport_transfer,
                    'room_service': resort.room_service,
                    'family_rooms': resort.family_rooms,
                }
            }
        })
