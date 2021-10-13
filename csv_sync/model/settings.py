from odoo import models, fields, exceptions, api, _
import logging
from datetime import datetime, date


class settings(models.TransientModel):
    _inherit = 'res.config.settings'

    delimiter = fields.Selection([(',', 'comma'), ('; ', 'semicolon'),('|', 'pipe')],
                                 required=True, default=',', string="Delimiter")
    local_path = fields.Binary('Local Path')
