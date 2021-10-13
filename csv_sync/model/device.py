from odoo import api, fields, models
from datetime import datetime, date


class device(models.Model):
    _name = 'device.sync'
    _rec_name = 'name'

    id = fields.Integer(string="Device ID")
    name = fields.Char(string="Name", size=32)
    description = fields.Char(string="Description", size=128)
    code = fields.Char(string="Code", size=30)
    expire_date = fields.Datetime(string="Expire Date")
    state = fields.Selection([('enabled', 'Enabled'), ('disabled', 'Disabled'), ('deleted', 'Deleted')],
                             required=True, default='enabled')

    # sql constraint to unique field
    _sql_constraints = [
        ('code_uniq', 'unique (code)', 'Code must be unique.')
    ]

    # expire date is past state must be deleted
    @api.onchange('expire_date')
    def onchange_date_range_id(self):
        if self.expire_date:
            today_date = date.today().strftime('%Y-%m-%d')
            expire_date = str(self.expire_date.date())
            if expire_date < today_date:
                self.state = 'disabled'
