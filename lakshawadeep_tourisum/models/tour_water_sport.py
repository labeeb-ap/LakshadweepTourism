from odoo import models, fields


class TourWaterSport(models.Model):
    _name = 'tour.water.sport'
    _description = 'Water Sport'

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

    price = fields.Float()

    description = fields.Text()

    active = fields.Boolean(default=True)

    booking_ids = fields.One2many(
        'tour.water.sport.booking',
        'water_sport_id'
    )





from odoo import models, fields, api


class TourWaterSportBooking(models.Model):
    _name = 'tour.water.sport.booking'
    _description = 'Water Sport Booking'
    _rec_name = 'booking_no'

    booking_no = fields.Char(
        default='New',
        readonly=True
    )

    water_sport_id = fields.Many2one(
        'tour.water.sport',
        required=True
    )

    customer_id = fields.Many2one(
        'res.partner',
        required=True
    )

    booking_date = fields.Date(
        required=True
    )

    participants = fields.Integer(
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
                'tour.water.sport.booking'
            ) or 'New'

        return super().create(vals)