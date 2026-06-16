from odoo import http
from odoo.http import request

from ..utils.jwt_helper import verify_token


class ShopController(http.Controller):

    @http.route(
        '/api/shops',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def shops(self, **kwargs):

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

        shops = request.env[
            'tour.shop'
        ].sudo().search(domain)

        base_url = request.env[
            'ir.config_parameter'
        ].sudo().get_param(
            'web.base.url'
        )

        data = []

        for shop in shops:

            image_url = None

            if shop.image:
                image_url = (
                    f"{base_url}/api/shop/image/{shop.id}"
                )

            data.append({
                'id': shop.id,
                'name': shop.name,
                'island_id': shop.island_id.code,
                'island_name': shop.island_id.name,
                'image': image_url,
                'category': shop.category,
                'description': shop.description or '',
            })

        return request.make_json_response({
            'success': True,
            'message': 'Shops fetched successfully',
            'data': data
        })