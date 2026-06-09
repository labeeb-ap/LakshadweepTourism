from odoo import models, fields


class TourIsland(models.Model):
    _name = 'tour.island'
    _description = 'Island'
    _order = 'sequence, name'

    name = fields.Char(
        string='Island Name',
        required=True
    )



    image = fields.Image(
        string='Image'
    )

    description = fields.Text(
        string='Description'
    )

    sequence = fields.Integer(
        default=10
    )

    active = fields.Boolean(
        default=True
    )



