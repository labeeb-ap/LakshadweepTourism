from odoo import http
from odoo.http import request
import json

from ..utils.jwt_helper import verify_token


class PackageBookingController(http.Controller):

    @http.route(
        '/api/book/package',
        type='http',
        auth='public',
        methods=['POST'],
        csrf=False
    )
    def book_package(self, **kwargs):

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

        package_id = data.get('package_id')
        travel_date = data.get('travel_date')
        persons = data.get('persons', 1)
        description = data.get('description', '')

        if not package_id:
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Package is required'
                },
                status=400
            )

        if not travel_date:
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Travel date is required'
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

        package = request.env[
            'tour.package'
        ].sudo().browse(
            package_id
        )

        if not package.exists():
            return request.make_json_response(
                {
                    'success': False,
                    'message': 'Package not found'
                },
                status=404
            )

        booking = request.env[
            'tour.package.booking'
        ].sudo().create({
            'package_id': package.id,
            'customer_id': customer.id,
            'travel_date': travel_date,
            'persons': persons,
            'description': description,
            'state': 'booked'
        })

        return request.make_json_response({
            'success': True,
            'message': 'Package booked successfully',
            'data': {
                'booking_id': booking.id,
                'package_id': booking.package_id.id,
                'package_name': booking.package_id.name,
                'customer_id': booking.customer_id.id,
                'customer_name': booking.customer_id.name,
                'travel_date': str(booking.travel_date),
                'persons': booking.persons,
                'description': booking.description or '',
                'state': booking.state,
                'booking_datetime': (
                    booking.booking_datetime.strftime(
                        '%Y-%m-%d %H:%M:%S'
                    )
                    if booking.booking_datetime else ''
                )
            }
        })