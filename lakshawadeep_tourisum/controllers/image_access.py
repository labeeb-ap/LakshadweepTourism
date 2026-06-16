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




    @http.route(
        '/api/taxi/image/<int:taxi_id>',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def taxi_image(self, taxi_id):

        taxi = request.env[
            'tour.taxi'
        ].sudo().browse(taxi_id)

        if not taxi.exists() or not taxi.image:
            return request.not_found()

        return request.make_response(
            base64.b64decode(taxi.image),
            headers=[
                ('Content-Type', 'image/jpeg')
            ]
        )

    def water_sport_image(self, sport_id):

        sport = request.env[
            'tour.water.sport'
        ].sudo().browse(sport_id)

        if not sport.exists() or not sport.image:
            return request.not_found()

        return request.make_response(
            base64.b64decode(sport.image),
            headers=[
                ('Content-Type', 'image/jpeg')
            ]
        )

    @http.route(
        '/api/shop/image/<int:shop_id>',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def shop_image(self, shop_id):

        shop = request.env[
            'tour.shop'
        ].sudo().browse(shop_id)

        if not shop.exists() or not shop.image:
            return request.not_found()

        return request.make_response(
            base64.b64decode(shop.image),
            headers=[
                ('Content-Type', 'image/jpeg')
            ]
        )


    @http.route(
        '/api/restaurant/image/<int:restaurant_id>',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def restaurant_image(self, restaurant_id):

        restaurant = request.env[
            'tour.restaurant'
        ].sudo().browse(restaurant_id)

        if not restaurant.exists() or not restaurant.image:
            return request.not_found()

        return request.make_response(
            base64.b64decode(restaurant.image),
            headers=[
                ('Content-Type', 'image/jpeg')
            ]
        )


    @http.route(
        '/api/package/image/<int:package_id>',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def package_image(self, package_id):

        package = request.env[
            'tour.package'
        ].sudo().browse(package_id)

        if not package.exists() or not package.image:
            return request.not_found()

        return request.make_response(
            base64.b64decode(package.image),
            headers=[
                ('Content-Type', 'image/jpeg')
            ]
        )




    @http.route(
        '/api/resort/gallery/image/<int:image_id>',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def resort_gallery_image(self, image_id):

        image = request.env[
            'tour.resort.image'
        ].sudo().browse(image_id)

        if not image.exists() or not image.image:
            return request.not_found()

        return request.make_response(
            base64.b64decode(image.image),
            headers=[
                ('Content-Type', 'image/jpeg')
            ]
        )

    @http.route(
        '/api/beach-homestay/gallery/image/<int:image_id>',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def beach_homestay_gallery_image(self, image_id):

        image = request.env[
            'tour.beach.homestay.image'
        ].sudo().browse(image_id)

        if not image.exists() or not image.image:
            return request.not_found()

        return request.make_response(
            base64.b64decode(image.image),
            headers=[
                ('Content-Type', 'image/jpeg')
            ]
        )




    @http.route(
        '/api/homestay/gallery/image/<int:image_id>',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def homestay_gallery_image(self, image_id):

        image = request.env[
            'tour.homestay.image'
        ].sudo().browse(image_id)

        if not image.exists() or not image.image:
            return request.not_found()

        return request.make_response(
            base64.b64decode(image.image),
            headers=[
                ('Content-Type', 'image/jpeg')
            ]
        )



    @http.route(
        '/api/water-sport/gallery/image/<int:image_id>',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def water_sport_gallery_image(self, image_id):

        image = request.env[
            'tour.water.sport.image'
        ].sudo().browse(image_id)

        if not image.exists() or not image.image:
            return request.not_found()

        return request.make_response(
            base64.b64decode(image.image),
            headers=[
                ('Content-Type', 'image/jpeg')
            ]
        )



    @http.route(
        '/api/water-sport/image/<int:water_sport_id>',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def water_sport_image(self, water_sport_id):

        water_sport = request.env[
            'tour.water.sport'
        ].sudo().browse(
            water_sport_id
        )

        if not water_sport.exists() or not water_sport.image:
            return request.not_found()

        return request.make_response(
            base64.b64decode(water_sport.image),
            headers=[
                ('Content-Type', 'image/jpeg')
            ]
        )