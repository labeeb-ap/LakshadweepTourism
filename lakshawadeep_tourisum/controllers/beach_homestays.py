from odoo import http
from odoo.http import request

from ..utils.jwt_helper import verify_token


class BeachHomestayController(http.Controller):

    @http.route(
        '/api/beach-homestays',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def beach_homestays(self, **kwargs):

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
            'tour.beach.homestay'
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
                    f"{base_url}/api/beach-homestay/image/{homestay.id}"
                )

            data.append({
                'id': homestay.id,
                'name': homestay.name,
                'island_id': homestay.island_id.code,
                'island_name': homestay.island_id.name,
                'image': image_url,
                'price': homestay.price_per_night,
                'description': homestay.description or '',
            })

        return request.make_json_response({
            'success': True,
            'message': 'Beach Homestays fetched successfully',
            'data': data
        })











    @http.route(
        '/api/beach-homestay/<int:homestay_id>',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def beach_homestay_detail(self, homestay_id, **kwargs):

        payload = verify_token()

        if not payload:
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Invalid or expired token'
                },
                status=401
            )

        homestay = request.env[
            'tour.beach.homestay'
        ].sudo().search(
            [
                ('id', '=', homestay_id),
                ('active', '=', True)
            ],
            limit=1
        )

        if not homestay:
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Beach Homestay not found'
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

        if homestay.image:
            image_url = (
                f"{base_url}/api/beach-homestay/image/{homestay.id}"
            )

        # Gallery Images
        gallery_images = []

        for img in homestay.image_ids:
            gallery_images.append({
                'id': img.id,
                'name': img.name or '',
                'image_url': (
                    f"{base_url}/api/beach-homestay/gallery/image/{img.id}"
                )
            })

        return request.make_json_response({
            'success': True,
            'message': 'Beach Homestay details fetched successfully',
            'data': {
                'id': homestay.id,
                'name': homestay.name,

                'island_id': homestay.island_id.id,
                'island_code': homestay.island_id.code,
                'island_name': homestay.island_id.name,

                'image': image_url,
                'gallery_images': gallery_images,

                'price_per_night': homestay.price_per_night,
                'description': homestay.description or '',

                'checkin_time': homestay.checkin_time,
                'checkout_time': homestay.checkout_time,

                'amenities': {
                    'sea_view': homestay.sea_view,
                    'beach_access': homestay.beach_access,
                    'free_wifi': homestay.free_wifi,
                    'air_conditioning': homestay.air_conditioning,
                    'restaurant': homestay.restaurant,
                    'swimming_pool': homestay.swimming_pool,
                    'free_breakfast': homestay.free_breakfast,
                    'airport_transfer': homestay.airport_transfer,
                    'room_service': homestay.room_service,
                    'family_rooms': homestay.family_rooms,
                }
            }
        })