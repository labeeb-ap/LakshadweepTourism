from odoo import http
from odoo.http import request
import json

from ..utils.jwt_helper import verify_token


class TaxiBookingController(http.Controller):

    @http.route(
        '/api/book/taxi',
        type='http',
        auth='public',
        methods=['POST'],
        csrf=False
    )
    def book_taxi(self, **kwargs):

        payload = verify_token()

        if not payload:
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Invalid or expired token'
                },
                status=401
            )

        try:
            data = json.loads(
                request.httprequest.data.decode('utf-8')
            )
        except Exception:
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Invalid JSON payload'
                },
                status=400
            )

        taxi_id = data.get('taxi_id')
        booking_date = data.get('booking_date')
        pickup_location = data.get('pickup_location')
        drop_location = data.get('drop_location')
        passengers = data.get('passengers', 1)
        description = data.get('description', '')

        if not taxi_id:
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Taxi is required'
                },
                status=400
            )

        if not booking_date:
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Booking date is required'
                },
                status=400
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

        taxi = request.env[
            'tour.taxi'
        ].sudo().browse(
            taxi_id
        )

        if not taxi.exists():
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Taxi not found'
                },
                status=404
            )

        booking = request.env[
            'tour.taxi.booking'
        ].sudo().create({
            'taxi_id': taxi.id,
            'customer_id': customer.id,
            'booking_date': booking_date,
            'pickup_location': pickup_location,
            'drop_location': drop_location,
            'passengers': passengers,
            'description': description,
            'state': 'booked'
        })

        return request.make_json_response({
            'success': True,
            'message': 'Taxi booked successfully',
            'data': {
                'booking_id': booking.id,

                'taxi_id': booking.taxi_id.id,
                'taxi_name': booking.taxi_id.name,

                'customer_id': booking.customer_id.id,
                'customer_name': booking.customer_id.name,

                'booking_date': str(
                    booking.booking_date
                ),

                'pickup_location': (
                    booking.pickup_location or ''
                ),

                'drop_location': (
                    booking.drop_location or ''
                ),

                'passengers': booking.passengers,

                'description': (
                    booking.description or ''
                ),

                'state': booking.state,

                'booking_datetime': (
                    booking.booking_datetime.strftime(
                        '%Y-%m-%d %H:%M:%S'
                    )
                    if booking.booking_datetime
                    else ''
                )
            }
        })