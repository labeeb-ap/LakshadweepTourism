from odoo import http
from odoo.http import request
import json

from ..utils.jwt_helper import verify_token


class ResortBookingController(http.Controller):

    @http.route(
        '/api/book/resort',
        type='http',
        auth='public',
        methods=['POST'],
        csrf=False
    )
    def book_resort(self, **kwargs):

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

        resort_id = data.get('resort_id')
        check_in_date = data.get('check_in_date')
        check_out_date = data.get('check_out_date')
        guests = data.get('guests', 1)
        rooms = data.get('rooms', 1)
        description = data.get('description', '')

        if not resort_id:
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Resort is required'
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

        resort = request.env[
            'tour.resort'
        ].sudo().browse(
            resort_id
        )

        if not resort.exists():
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Resort not found'
                },
                status=404
            )

        booking = request.env[
            'tour.resort.booking'
        ].sudo().create({
            'resort_id': resort.id,
            'customer_id': customer.id,
            'check_in_date': check_in_date,
            'check_out_date': check_out_date,
            'guests': guests,
            'description': description,
            'rooms': rooms,
            'state': 'booked'
        })

        return request.make_json_response({
            'success': True,
            'message': 'Resort booked successfully',
            'data': {
                'booking_id': booking.id,
                'resort_id': booking.resort_id.id,
                'resort_name': booking.resort_id.name,
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