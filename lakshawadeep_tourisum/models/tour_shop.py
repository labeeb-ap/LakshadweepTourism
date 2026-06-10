from odoo import models, fields


class TourShop(models.Model):
    _name = 'tour.shop'
    _description = 'Local Shop'

    name = fields.Char(
        string='Shop Name',
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
        string='Image'
    )

    category = fields.Char(
        string='Category'
    )

    rating = fields.Float()

    reviews = fields.Integer()

    description = fields.Text()

    active = fields.Boolean(
        default=True
    )