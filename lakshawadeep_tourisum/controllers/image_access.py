from odoo import http
from odoo.http import request
import base64


class PublicImageController(http.Controller):

    @http.route(
        '/api/island/image/<int:island_id>',
        type='http',
        auth='public',
        csrf=False
    )
    def island_image(self, island_id, **kwargs):

        island = request.env['tour.island'].sudo().browse(island_id)

        if not island.exists() or not island.image:
            return request.not_found()

        return request.make_response(
            base64.b64decode(island.image),
            headers=[
                ('Content-Type', 'image/jpeg')
            ]
        )










    @http.route(
        '/api/resort/image/<int:resort_id>',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def resort_image(self, resort_id):

        resort = request.env[
            'tour.resort'
        ].sudo().browse(resort_id)

        if not resort.exists() or not resort.image:
            return request.not_found()

        return request.make_response(
            base64.b64decode(resort.image),
            headers=[
                ('Content-Type', 'image/jpeg')
            ]
        )




    @http.route(
        '/api/homestay/image/<int:homestay_id>',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )




    def homestay_image(self, homestay_id):

        homestay = request.env[
            'tour.homestay'
        ].sudo().browse(homestay_id)

        if not homestay.exists() or not homestay.image:
            return request.not_found()

        return request.make_response(
            base64.b64decode(homestay.image),
            headers=[
                ('Content-Type', 'image/jpeg')
            ]
        )








from odoo import http
from odoo.http import request
import base64


class BeachHomestayImageController(http.Controller):

    @http.route(
        '/api/beach-homestay/image/<int:homestay_id>',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def beach_homestay_image(self, homestay_id):

        homestay = request.env[
            'tour.beach.homestay'
        ].sudo().browse(homestay_id)

        if not homestay.exists() or not homestay.image:
            return request.not_found()

        return request.make_response(
            base64.b64decode(homestay.image),
            headers=[
                ('Content-Type', 'image/jpeg')
            ]
        )