from odoo import models, fields


class TourResort(models.Model):
    _name = 'tour.resort'
    _description = 'Resort'

    name = fields.Char(required=True)
    island_id = fields.Many2one('tour.island', required=True)
    image = fields.Binary()

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








from odoo import models, fields, api


class TourResortBooking(models.Model):
    _name = 'tour.resort.booking'
    _description = 'Resort Booking'
    _rec_name = 'booking_no'

    booking_no = fields.Char(
        string='Booking Number',
        default='New',
        readonly=True
    )

    resort_id = fields.Many2one(
        'tour.resort',
        required=True
    )

    customer_id = fields.Many2one(
        'res.partner',
        required=True
    )

    checkin_date = fields.Date(required=True)



    room_count = fields.Integer(default=1)

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
                'tour.resort.booking'
            ) or 'New'

        return super().create(vals)

