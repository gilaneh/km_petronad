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
    partner = fields.Many2one('res.partner')
    analysis = fields.Float()
    amount = fields.Integer()


