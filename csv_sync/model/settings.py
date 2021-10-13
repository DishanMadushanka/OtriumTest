from odoo import models, fields, exceptions, api, _
import logging
from datetime import datetime, date


class settings(models.Model):
    _name = 'setting.file'

    delimiter = fields.Selection([(',', 'comma'), ('; ', 'semicolon'), ('|', 'pipe')],
                                 required=True, default=',')
    local_path = fields.Char('Local Path')
    active = fields.Boolean(string="Active")
