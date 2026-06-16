from odoo import http
from odoo.http import request
import json

from ..utils.jwt_helper import verify_token


class WaterSportBookingController(http.Controller):

    @http.route(
        '/api/book/water-sport',
        type='http',
        auth='public',
        methods=['POST'],
        csrf=False
    )
    def book_water_sport(self, **kwargs):

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

        water_sport_id = data.get('water_sport_id')
        booking_date = data.get('booking_date')
        participants = data.get('participants', 1)
        description = data.get('description', '')

        if not water_sport_id:
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Water Sport is required'
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

        water_sport = request.env[
            'tour.water.sport'
        ].sudo().browse(
            water_sport_id
        )

        if not water_sport.exists():
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Water Sport not found'
                },
                status=404
            )

        booking = request.env[
            'tour.water.sport.booking'
        ].sudo().create({
            'water_sport_id': water_sport.id,
            'customer_id': customer.id,
            'booking_date': booking_date,
            'participants': participants,
            'description': description,
            'state': 'booked'
        })

        return request.make_json_response({
            'success': True,
            'message': 'Water Sport booked successfully',
            'data': {
                'booking_id': booking.id,

                'water_sport_id': booking.water_sport_id.id,
                'water_sport_name': booking.water_sport_id.name,

                'customer_id': booking.customer_id.id,
                'customer_name': booking.customer_id.name,

                'booking_date': str(
                    booking.booking_date
                ),

                'participants': booking.participants,

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