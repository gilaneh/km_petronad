# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime
import jdatetime
import json
from odoo.exceptions import ValidationError, UserError


class KmPetronadStorageTanks(models.Model):
    _name = 'km_petronad.storage_tanks'

    name = fields.Char(require=True )
    tank_date = fields.Datetime(default=lambda self: datetime.now())
    location = fields.Char(require=False )
    asset_id = fields.Char(require=False )
    fluid = fields.Many2one('km_petronad.fluids', require=True )
    production_unit = fields.Many2one('km_petronad.production_unit', require=True )
    capacity = fields.Integer(require=True)
    amount = fields.Integer()
    unit = fields.Selection([('kg', 'Kg'), ('ton', 'Ton')], default='kg', required=True)
    description = fields.Text()

#     todo: there

    # @api.onchange('fluid')
    # def fluid_canged(self):
    #     if self.amount:
    #         raise ValidationError(_(f'The tank is not empty'))

class KmPetronadTankOperations(models.Model):
    _name = 'km_petronad.tank_operations'

    name = fields.Char(require=True)
    code = fields.Char(require=True)
    fluid = fields.Many2many('km_petronad.fluids', require=True )
