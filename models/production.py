# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime
import jdatetime
import json


class KmPetronadProductionUnit(models.Model):
    _name = 'km_petronad.production_unit'

    name = fields.Char( required=True)
    company = fields.Many2one( 'res.company', required=True)
    description = fields.Text( )

class KmPetronadProductionRecord(models.Model):
    _name = 'km_petronad.production_record'
    _rec_name = 'data_date'
    _order = 'data_date desc'

    data_date = fields.Date()
    fluid = fields.Many2one('km_petronad.fluids')
    tank = fields.Many2one('km_petronad.storage_tanks')
    shift = fields.Selection([('day', 'Day'), ('night', 'Night')], required=True)
    shift_group = fields.Selection([('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')], required=True)
    register_type = fields.Selection([('production', 'Production'), ('sale', 'Sale'), ('feed_receive', 'Feed Receive'),], )
    partner = fields.Many2one('res.partner')
    transporter = fields.Many2one('res.partner')
    transport_type = fields.Selection([('tanker', 'Tanker'), ('barrel', 'Barrel')], )
    barrel_quantity = fields.Integer()
    barrel_weight = fields.Integer()
    driver = fields.Char()
    car_plate = fields.Char()
    permit_no = fields.Char()
    analysis = fields.Float()
    amount = fields.Integer()
    unit = fields.Selection([('kg', 'Kg'), ('ton', 'Ton')], default='kg', required=True)



