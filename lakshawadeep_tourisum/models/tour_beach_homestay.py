from odoo import models, fields , api


class TourBeachHomestay(models.Model):
    _name = 'tour.beach.homestay'
    _description = 'Beach Homestay'

    name = fields.Char(required=True)

    island_id = fields.Many2one(
        'tour.island',
        required=True
    )

    image = fields.Image()

    vendor_id = fields.Many2one(
        'res.partner',
        domain=[('is_vendor', '=', True)]
    )



    price_per_night = fields.Float()

    description = fields.Text()

    active = fields.Boolean(default=True)

    booking_ids = fields.One2many(
        'tour.beach.homestay.booking',
        'homestay_id'
    )


class TourBeachHomestayBooking(models.Model):
    _name = 'tour.beach.homestay.booking'
    _description = 'Beach Homestay Booking'
    _rec_name = 'booking_no'

    booking_no = fields.Char(
        default='New',
        readonly=True
    )

    homestay_id = fields.Many2one(
        'tour.beach.homestay',
        required=True
    )

    customer_id = fields.Many2one(
        'res.partner',
        required=True
    )

    checkin_date = fields.Date(
        required=True
    )

    room_count = fields.Integer(
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
                'tour.beach.homestay.booking'
            ) or 'New'

        return super().create(vals)