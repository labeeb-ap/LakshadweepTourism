from odoo import models, fields




class TourHomestay(models.Model):
    _name = 'tour.homestay'
    _description = 'Homestay'

    name = fields.Char(required=True)

    island_id = fields.Many2one(
        'tour.island',
        required=True
    )

    image = fields.Image()

    image_ids = fields.One2many(
        'tour.homestay.image',
        'homestay_id',
        string='Gallery Images'
    )

    vendor_id = fields.Many2one(
        'res.partner',
        domain=[('is_vendor', '=', True)]
    )

    description = fields.Text()

    room_count = fields.Integer()

    checkin_time = fields.Float()
    checkout_time = fields.Float()

    price_per_night = fields.Float()

    active = fields.Boolean(default=True)

    booking_ids = fields.One2many(
        'tour.homestay.booking',
        'homestay_id'
    )

    # Amenities

    sea_view = fields.Boolean(string='Sea View')

    beach_access = fields.Boolean(string='Beach Access')

    free_wifi = fields.Boolean(string='Free WiFi')

    air_conditioning = fields.Boolean(string='Air Conditioning')

    restaurant = fields.Boolean(string='Restaurant')

    swimming_pool = fields.Boolean(string='Swimming Pool')

    free_breakfast = fields.Boolean(string='Free Breakfast')

    airport_transfer = fields.Boolean(string='Airport Transfer')

    room_service = fields.Boolean(string='Room Service')

    family_rooms = fields.Boolean(string='Family Rooms')










from odoo import models, fields, api


class TourHomestayBooking(models.Model):
    _name = 'tour.homestay.booking'
    _description = 'Homestay Booking'

    homestay_id = fields.Many2one(
        'tour.homestay',
        required=True
    )

    customer_id = fields.Many2one(
        'res.partner',
        required=True,
        readonly=True
    )

    check_in_date = fields.Date(
        required=True
    )

    check_out_date = fields.Date(
        required=True
    )

    guests = fields.Integer(
        default=1,
        required=True
    )

    rooms = fields.Integer(
        default=1,
        required=True
    )
    description = fields.Text(
        string='Description'
    )

    amount = fields.Float()

    booking_datetime = fields.Datetime(
        string='Booking Time',
        default=fields.Datetime.now,
        readonly=True
    )

    state = fields.Selection([
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled')
    ], default='booked', required=True)




from odoo import models, fields


class TourHomestayImage(models.Model):
    _name = 'tour.homestay.image'
    _description = 'Homestay Image'

    name = fields.Char()

    homestay_id = fields.Many2one(
        'tour.homestay',
        required=True,
        ondelete='cascade'
    )

    image = fields.Image(
        required=True
    )