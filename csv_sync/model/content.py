from odoo import models, fields, exceptions, api, _
import logging
from datetime import datetime, date


class content(models.Model):
    _name = 'content.sync'
    _rec_name = 'name'

    id = fields.Integer(string="Content ID")
    name = fields.Char(string="Name", size=100)
    description = fields.Char(string="Description", size=128)
    device = fields.Many2one('device.sync', string="Device")
    expire_date = fields.Datetime(string="Expire Date")
    state = fields.Selection([('enabled', 'Enabled'), ('disabled', 'Disabled'), ('deleted', 'Deleted')],
                             required=True, default='enabled')

    # expire date is past state must be deleted
    @api.onchange('expire_date')
    def onchange_date_range_id(self):
        if self.expire_date:
            today_date = date.today().strftime('%Y-%m-%d')
            expire_date = str(self.expire_date.date())
            if expire_date < today_date:
                self.state = 'disabled'
