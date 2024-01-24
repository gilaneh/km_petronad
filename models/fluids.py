# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime
import jdatetime
import json


class KmPetronadFluids(models.Model):
    _name = 'km_petronad.fluids'

    name = fields.Char(require=True )
    description = fields.Text()

class KmPetronadFluidMove(models.Model):
    _name = 'km_petronad.fluid_move'

    move_date = fields.Datetime(require=True )
    fluid = fields.Many2one('km_petronad.fluids', require=True)
    amount = fields.Integer()
    operation = fields.Selection([('feed_usage', 'Feed Usage'),
                                  ('feed_receive', 'Feed Receive'),
                                  ('production', 'Production'),
                                  ('sending', 'Sending'),
                                  ('movement', 'Movement'),
                                  ], default='production', require=True)
    sending_types = fields.Selection([('sale', 'Sale'),('transfer', 'Transfer'),], default='sale', require=True)
    quality_analysis = fields.Float()
    vendor = fields.Many2one('res.partners')
    buyer = fields.Many2one('res.partners')
    description = fields.Text()

