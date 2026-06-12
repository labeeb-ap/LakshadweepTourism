from odoo import http
from odoo.http import request

from ..utils.jwt_helper import verify_token


class PackageController(http.Controller):

    @http.route(
        '/api/packages',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def packages(self, **kwargs):

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

        packages = request.env[
            'tour.package'
        ].sudo().search(domain)

        base_url = request.env[
            'ir.config_parameter'
        ].sudo().get_param(
            'web.base.url'
        )

        data = []

        for package in packages:

            image_url = None

            if package.image:
                image_url = (
                    f"{base_url}/api/package/image/{package.id}"
                )

            data.append({
                'id': package.id,
                'name': package.name,
                'island_id': package.island_id.code,
                'island_name': package.island_id.name,
                'image': image_url,
                'duration': package.duration,
                'price': package.price,
                'description': package.description or '',
            })

        return request.make_json_response({
            'success': True,
            'message': 'Packages fetched successfully',
            'data': data
        })