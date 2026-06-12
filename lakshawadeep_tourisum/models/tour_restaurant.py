







from odoo import models, fields












class TourRestaurant(models.Model):
    _name = 'tour.restaurant'
    _description = 'Restaurant'

    name = fields.Char(
        required=True
    )

    island_id = fields.Many2one(
        'tour.island',
        required=True
    )

    vendor_id = fields.Many2one(
        'res.partner',
        domain=[('is_vendor', '=', True)]
    )

    image = fields.Image()

    cuisine_ids = fields.Many2many(
        'tour.cuisine',
        string='Cuisines'
    )

    description = fields.Text()

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