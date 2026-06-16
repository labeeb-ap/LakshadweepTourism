from odoo import models, fields


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
    image_ids = fields.One2many(
        'tour.water.sport.image',
        'water_sport_id',
        string='Gallery Images'
    )

    vendor_id = fields.Many2one(
        'res.partner',
        domain=[('is_vendor', '=', True)]
    )

    price = fields.Float()

    duration = fields.Char(
        help='Example: 3-4 Hours'
    )

    age_limit = fields.Char(
        string='Age Limit',
        help='Example: 10+ Years'
    )

    group_size = fields.Char(
        string='Group Size',
        help='Example: 2-4 People'
    )

    include_ids = fields.Many2many(
        'tour.water.sport.include',
        string='Included Activities'
    )

    description = fields.Text()

    active = fields.Boolean(
        default=True
    )

    booking_ids = fields.One2many(
        'tour.water.sport.booking',
        'water_sport_id'
    )



from odoo import models, fields


class TourWaterSportInclude(models.Model):
    _name = 'tour.water.sport.include'
    _description = 'Water Sport Include'

    name = fields.Char(
        required=True
    )

    active = fields.Boolean(
        default=True
    )




from odoo import models, fields


class TourWaterSportImage(models.Model):
    _name = 'tour.water.sport.image'
    _description = 'Water Sport Gallery Image'

    water_sport_id = fields.Many2one(
        'tour.water.sport',
        required=True,
        ondelete='cascade'
    )

    name = fields.Char()

    image = fields.Image(
        required=True
    )










from odoo import models, fields, api


class TourWaterSportBooking(models.Model):
    _name = 'tour.water.sport.booking'
    _description = 'Water Sport Booking'



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







