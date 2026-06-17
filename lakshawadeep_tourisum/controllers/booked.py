import json

from odoo import http
from odoo.http import request

from ..utils.jwt_helper import verify_token


class MyBookingController(http.Controller):

    @http.route(
        '/api/my-bookings',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def my_bookings(self, **kwargs):

        payload = verify_token()

        if not payload:
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Invalid or expired token'
                },
                status=401
            )

        user = request.env[
            'res.users'
        ].sudo().browse(
            payload.get('uid')
        )

        if not user.exists():
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'User not found'
                },
                status=404
            )

        customer = user.partner_id

        bookings = []

        # =====================================================
        # RESORT BOOKINGS
        # =====================================================

        for rec in request.env[
            'tour.resort.booking'
        ].sudo().search([
            ('customer_id', '=', customer.id)
        ]):

            bookings.append({
                'booking_id': rec.id,
                'type': 'resort',
                'name': rec.resort_id.name,
                'booking_datetime': rec.booking_datetime,
                'state': rec.state,
            })

        # =====================================================
        # HOMESTAY BOOKINGS
        # =====================================================

        for rec in request.env[
            'tour.homestay.booking'
        ].sudo().search([
            ('customer_id', '=', customer.id)
        ]):

            bookings.append({
                'booking_id': rec.id,
                'type': 'homestay',
                'name': rec.homestay_id.name,
                'booking_datetime': rec.booking_datetime,
                'state': rec.state,
            })

        # =====================================================
        # BEACH HOMESTAY BOOKINGS
        # =====================================================

        for rec in request.env[
            'tour.beach.homestay.booking'
        ].sudo().search([
            ('customer_id', '=', customer.id)
        ]):

            bookings.append({
                'booking_id': rec.id,
                'type': 'beach_homestay',
                'name': rec.homestay_id.name,
                'booking_datetime': rec.booking_datetime,
                'state': rec.state,
            })

        # =====================================================
        # PACKAGE BOOKINGS
        # =====================================================

        for rec in request.env[
            'tour.package.booking'
        ].sudo().search([
            ('customer_id', '=', customer.id)
        ]):

            bookings.append({
                'booking_id': rec.id,
                'type': 'package',
                'name': rec.package_id.name,
                'booking_datetime': rec.booking_datetime,
                'state': rec.state,
            })

        # =====================================================
        # WATER SPORT BOOKINGS
        # =====================================================

        for rec in request.env[
            'tour.water.sport.booking'
        ].sudo().search([
            ('customer_id', '=', customer.id)
        ]):

            bookings.append({
                'booking_id': rec.id,
                'type': 'water_sport',
                'name': rec.water_sport_id.name,
                'booking_datetime': rec.booking_datetime,
                'state': rec.state,
            })

        # =====================================================
        # TAXI BOOKINGS
        # =====================================================

        for rec in request.env[
            'tour.taxi.booking'
        ].sudo().search([
            ('customer_id', '=', customer.id)
        ]):

            bookings.append({
                'booking_id': rec.id,
                'type': 'taxi',
                'name': rec.taxi_id.name,
                'booking_datetime': rec.booking_datetime,
                'state': rec.state,
            })

        # =====================================================
        # SORT BY BOOKING DATETIME DESC
        # =====================================================

        bookings = sorted(
            bookings,
            key=lambda x: x['booking_datetime'] or '',
            reverse=True
        )

        # =====================================================
        # FORMAT DATETIME
        # =====================================================

        result = []

        for booking in bookings:

            result.append({
                'booking_id': booking['booking_id'],
                'type': booking['type'],
                'name': booking['name'],
                'booking_datetime': (
                    booking['booking_datetime'].strftime(
                        '%Y-%m-%d %H:%M:%S'
                    )
                    if booking['booking_datetime']
                    else ''
                ),
                'state': booking['state'],
            })

        return request.make_json_response({
            'success': True,
            'customer_id': customer.id,
            'customer_name': customer.name,
            'total_bookings': len(result),
            'data': result
        })
