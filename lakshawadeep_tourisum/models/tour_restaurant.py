







from odoo import models, fields








from odoo import models, fields


class TourRestaurant(models.Model):
    _name = 'tour.restaurant'
    _description = 'Restaurant'
    _rec_name = 'name'

    name = fields.Char(
        required=True
    )

    island_id = fields.Many2one(
        'tour.island',
        required=True,
        ondelete='cascade'
    )

    vendor_id = fields.Many2one(
        'res.partner',
        string='Vendor',
        domain=[('is_vendor', '=', True)]
    )

    image = fields.Image(
        string='Image'
    )

    cuisine_ids = fields.Many2many(
        'tour.cuisine',
        string='Cuisines'
    )

    description = fields.Text(
        string='Description'
    )

    opening_time = fields.Char("Opening Time")
    opening_period = fields.Selection([
        ('am', 'AM'),
        ('pm', 'PM')
    ], string="Opening Period",default='am')

    closing_time = fields.Char("Closing Time")
    closing_period = fields.Selection([
        ('am', 'AM'),
        ('pm', 'PM')
    ], string="Closing Period",defualt="pm")

    opening_note = fields.Char(
        string='Opening Hours Note',
        help='Example: Open Daily, Closed on Fridays'
    )

    # Contact
    phone = fields.Char(
        string='Phone'
    )

    # Location
    address = fields.Text(
        string='Address'
    )

    latitude = fields.Float(
        string='Latitude',
        digits=(10, 7)
    )

    longitude = fields.Float(
        string='Longitude',
        digits=(10, 7)
    )

    active = fields.Boolean(
        default=True
    )















from odoo import models, fields


class TourCuisine(models.Model):
    _name = 'tour.cuisine'
    _description = 'Cuisine'

    name = fields.Char(
        required=True
    )

    active = fields.Boolean(
        default=True
    )