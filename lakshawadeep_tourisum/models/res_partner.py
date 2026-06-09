from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_customer = fields.Boolean(
        string='Customer',
        default=False
    )

    is_vendor = fields.Boolean(
        string='Vendor',
        default=False
    )