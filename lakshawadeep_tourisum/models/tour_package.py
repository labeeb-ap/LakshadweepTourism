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

    service_ids = fields.Many2many(
        'tour.package.service',
        string='Included Services'
    )

    active = fields.Boolean(
        default=True
    )

    booking_ids = fields.One2many(
        'tour.package.booking',
        'package_id'
    )


from odoo import models, fields


class TourPackageService(models.Model):
    _name = 'tour.package.service'
    _description = 'Package Service'

    name = fields.Char(
        required=True
    )

    active = fields.Boolean(
        default=True
    )


from odoo import models, fields, api


class TourPackageBooking(models.Model):
    _name = 'tour.package.booking'
    _description = 'Package Booking'

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
