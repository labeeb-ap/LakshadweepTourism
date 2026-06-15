from odoo import models, fields, api


class TourBeachHomestay(models.Model):
    _name = 'tour.beach.homestay'
    _description = 'Beach Homestay'

    name = fields.Char(required=True)

    island_id = fields.Many2one(
        'tour.island',
        required=True
    )

    image = fields.Image()
    image_ids = fields.One2many(
        'tour.beach.homestay.image',
        'homestay_id',
        string='Gallery Images'
    )

    vendor_id = fields.Many2one(
        'res.partner',
        domain=[('is_vendor', '=', True)]
    )
    checkin_time = fields.Float()
    checkout_time = fields.Float()

    price_per_night = fields.Float()

    description = fields.Text()

    active = fields.Boolean(default=True)

    booking_ids = fields.One2many(
        'tour.beach.homestay.booking',
        'homestay_id'
    )

    sea_view = fields.Boolean()
    beach_access = fields.Boolean()
    free_wifi = fields.Boolean()
    air_conditioning = fields.Boolean()
    restaurant = fields.Boolean()
    swimming_pool = fields.Boolean()
    free_breakfast = fields.Boolean()
    airport_transfer = fields.Boolean()
    room_service = fields.Boolean()
    family_rooms = fields.Boolean()


class TourBeachHomestayBooking(models.Model):
    _name = 'tour.beach.homestay.booking'
    _description = 'Beach Homestay Booking'

    homestay_id = fields.Many2one(
        'tour.beach.homestay',
        required=True,
        ondelete='cascade'
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


class TourBeachHomestayImage(models.Model):
    _name = 'tour.beach.homestay.image'
    _description = 'Beach Homestay Image'

    name = fields.Char()

    homestay_id = fields.Many2one(
        'tour.beach.homestay',
        required=True,
        ondelete='cascade'
    )

    image = fields.Image(
        required=True
    )
