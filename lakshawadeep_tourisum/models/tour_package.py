
from odoo import models, fields


class TourPackage(models.Model):
    _name = 'tour.package'
    _description = 'Tour Package'

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

    duration = fields.Char()

    price = fields.Float()

    description = fields.Text()

    active = fields.Boolean(default=True)

    booking_ids = fields.One2many(
        'tour.package.booking',
        'package_id'
    )



























from odoo import models, fields, api


class TourPackageBooking(models.Model):
    _name = 'tour.package.booking'
    _description = 'Package Booking'
    _rec_name = 'booking_no'

    booking_no = fields.Char(
        default='New',
        readonly=True
    )

    package_id = fields.Many2one(
        'tour.package',
        required=True
    )

    customer_id = fields.Many2one(
        'res.partner',
        required=True
    )

    travel_date = fields.Date(
        required=True
    )

    persons = fields.Integer(
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
                'tour.package.booking'
            ) or 'New'

        return super().create(vals)