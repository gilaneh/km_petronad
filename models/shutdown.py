# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
import jdatetime
import json
TEHRAN_TIME = 3.5

class KmPetronadShutdown(models.Model):
    _name = 'km_petronad.shutdown'

    shutdown_date = fields.Date(required=True, default=lambda self: datetime.now() - timedelta(hours=TEHRAN_TIME) )
    shutdown_time = fields.Integer( required=True)
    fluid = fields.Many2one('km_petronad.fluids', required=True)
    shutdown_type = fields.Many2one('km_petronad.shutdown_type', required=True)
    description = fields.Text()


class KmPetronadShutdownType(models.Model):
    _name = 'km_petronad.shutdown_type'

    name = fields.Char(require=True)
