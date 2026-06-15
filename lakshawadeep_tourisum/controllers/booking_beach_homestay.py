from odoo import http
from odoo.http import request
import json

from ..utils.jwt_helper import verify_token


class BeachHomestayBookingController(http.Controller):

    @http.route(
        '/api/book/beach-homestay',
        type='http',
        auth='public',
        methods=['POST'],
        csrf=False
    )
    def book_beach_homestay(self, **kwargs):

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

        homestay_id = data.get('homestay_id')
        check_in_date = data.get('check_in_date')
        check_out_date = data.get('check_out_date')
        guests = data.get('guests', 1)
        rooms = data.get('rooms', 1)
        description = data.get('description', '')

        if not homestay_id:
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Beach Homestay is required'
                },
                status=400
            )

        if not check_in_date:
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Check-in date is required'
                },
                status=400
            )

        if not check_out_date:
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Check-out date is required'
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

        homestay = request.env[
            'tour.beach.homestay'
        ].sudo().browse(
            homestay_id
        )

        if not homestay.exists():
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Beach Homestay not found'
                },
                status=404
            )

        booking = request.env[
            'tour.beach.homestay.booking'
        ].sudo().create({
            'homestay_id': homestay.id,
            'customer_id': customer.id,
            'check_in_date': check_in_date,
            'check_out_date': check_out_date,
            'guests': guests,
            'rooms': rooms,
            'description': description,
            'state': 'booked'
        })

        return request.make_json_response({
            'success': True,
            'message': 'Beach Homestay booked successfully',
            'data': {
                'booking_id': booking.id,
                'homestay_id': booking.homestay_id.id,
                'homestay_name': booking.homestay_id.name,
                'customer_id': booking.customer_id.id,
                'customer_name': booking.customer_id.name,
                'check_in_date': booking.check_in_date,
                'check_out_date': booking.check_out_date,
                'guests': booking.guests,
                'rooms': booking.rooms,
                'description': booking.description,
                'state': booking.state
            }
        })