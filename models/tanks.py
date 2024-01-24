# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime
import jdatetime
import json


class KmPetronadStorageTanks(models.Model):
    _name = 'km_petronad.storage_tanks'

    name = fields.Char(require=True )
    tank_date = fields.Datetime(default=lambda self: datetime.now())
    location = fields.Char(require=False )
    asset_id = fields.Char(require=False )
    fluid = fields.Many2one('km_petronad.fluids', require=True )
    capacity = fields.Integer(require=True)
    description = fields.Text()

#     todo: there

