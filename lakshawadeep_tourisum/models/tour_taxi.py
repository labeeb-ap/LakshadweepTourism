from odoo import models, fields


class TourTaxi(models.Model):
    _name = 'tour.taxi'
    _description = 'Taxi Service'

    name = fields.Char(
        string='Vehicle Name',
        required=True
    )

    island_id = fields.Many2one(
        'tour.island',
        string='Island',
        required=True
    )

    vendor_id = fields.Many2one(
        'res.partner',
        string='Vendor',
        domain=[('is_vendor', '=', True)]
    )

    image = fields.Image(
        string='Vehicle Image'
    )

    vehicle_type = fields.Char(
        string='Vehicle Type'
    )

    seater = fields.Integer(
        string='Seating Capacity'
    )

    ac = fields.Boolean(
        string='AC Available',
        default=True
    )

    description = fields.Text()

    active = fields.Boolean(
        default=True
    )

    booking_ids = fields.One2many(
        'tour.taxi.booking',
        'taxi_id'
    )
    feature_ids = fields.Many2many(
        'tour.taxi.feature',
        string='Vehicle Features'
    )












class TourTaxiFeature(models.Model):
    _name = 'tour.taxi.feature'
    _description = 'Taxi Feature'

    name = fields.Char(
        required=True
    )

    active = fields.Boolean(
        default=True
    )










from odoo import models, fields, api


class TourTaxiBooking(models.Model):
    _name = 'tour.taxi.booking'
    _description = 'Taxi Booking'



    taxi_id = fields.Many2one(
        'tour.taxi',
        required=True
    )

    customer_id = fields.Many2one(
        'res.partner',
        required=True
    )

    booking_date = fields.Date(
        required=True
    )

    pickup_location = fields.Char()

    drop_location = fields.Char()

    passengers = fields.Integer(
    )

    description = fields.Text(
        string='Description'
    )

    state = fields.Selection([
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled')
    ], default='booked', required=True)

    booking_datetime = fields.Datetime(
        string='Booking Time',
        default=fields.Datetime.now,
        readonly=True
    )



