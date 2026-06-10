from odoo import models, fields


class TourIsland(models.Model):
    _name = 'tour.island'
    _description = 'Island'
    _order = 'code, name'

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

    code = fields.Integer(
        default=0
    )

    active = fields.Boolean(
        default=True
    )



