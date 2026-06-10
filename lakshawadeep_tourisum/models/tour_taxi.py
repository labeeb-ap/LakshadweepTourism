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










from odoo import models, fields, api


class TourTaxiBooking(models.Model):
    _name = 'tour.taxi.booking'
    _description = 'Taxi Booking'
    _rec_name = 'booking_no'

    booking_no = fields.Char(
        default='New',
        readonly=True
    )

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
        default=1
    )

    amount = fields.Float()

    state = fields.Selection([
        ('draft', 'Draft'),
        ('requested', 'Requested'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='draft')

    @api.model
    def create(self, vals):
        if vals.get('booking_no', 'New') == 'New':
            vals['booking_no'] = self.env[
                'ir.sequence'
            ].next_by_code(
                'tour.taxi.booking'
            ) or 'New'

        return super().create(vals)