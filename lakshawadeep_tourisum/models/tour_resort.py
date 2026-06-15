from odoo import models, fields


class TourResort(models.Model):
    _name = 'tour.resort'
    _description = 'Resort'

    name = fields.Char(required=True)
    island_id = fields.Many2one('tour.island', required=True)
    image = fields.Binary()
    image_ids = fields.One2many(
        'tour.resort.image',
        'resort_id',
        string='Gallery Images'
    )

    vendor_id = fields.Many2one(
        'res.partner',
        string='Vendor',
        domain=[('is_vendor', '=', True)]
    )

    description = fields.Text()

    room_count = fields.Integer()

    checkin_time = fields.Float()
    checkout_time = fields.Float()

    price_per_night = fields.Float()

    active = fields.Boolean(default=True)

    booking_ids = fields.One2many(
        'tour.resort.booking',
        'resort_id'
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


from odoo import models, fields


class TourResortBooking(models.Model):
    _name = 'tour.resort.booking'
    _description = 'Resort Booking'
    _order = 'id desc'

    resort_id = fields.Many2one(
        'tour.resort',
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

    state = fields.Selection([
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled')
    ], default='booked', required=True)

    booking_datetime = fields.Datetime(
        string='Booking Time',
        default=fields.Datetime.now,
        readonly=True
    )







from odoo import models, fields

class TourResortImage(models.Model):
    _name = 'tour.resort.image'
    _description = 'Resort Gallery Image'

    resort_id = fields.Many2one(
        'tour.resort',
        string='Resort',
        required=True,
        ondelete='cascade'
    )

    name = fields.Char()

    image = fields.Image(
        string='Image',
        required=True
    )

