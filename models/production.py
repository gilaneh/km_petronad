# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
import jdatetime
import json
from odoo.exceptions import AccessError, ValidationError, MissingError, UserError
TEHRAN_TIME = 3.5
EDIT_CONSTRAINT_DAYS = 1


class KmPetronadProductionRecord(models.Model):
    _name = 'km_petronad.production_record'
    _rec_name = 'data_date'
    _order = 'data_date desc'

    data_date = fields.Date()
    fluid = fields.Many2one('km_petronad.fluids')
    tank = fields.Many2one('km_petronad.storage_tanks')
    shift = fields.Selection([('day', 'Day'), ('night', 'Night')], )
    shift_group = fields.Selection([('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')], )
    register_type = fields.Selection([('production', 'Production'),
                                      ('sale', 'Sale'),
                                      ('feed_receive', 'Feed Receive'),
                                      ('feed_usage', 'Feed Usage'),], )
    partner = fields.Many2one('res.partner', string='Vendor/Buyer')
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

    def write(self, vals):
        if self.create_date + timedelta(days=EDIT_CONSTRAINT_DAYS) < datetime.now():
            raise ValidationError(_(f'This record is not editable. \n    It is {(datetime.now() - self.create_date).days} day(s) old.'))

        return super(KmPetronadProductionRecord, self).write(vals)


class KmPetronadProductionPlan(models.Model):
    _name = 'km_petronad.production_plan'

    data_date = fields.Date(required=True, default=lambda self: datetime.now() - timedelta(hours=TEHRAN_TIME) )
    fluid = fields.Many2one( 'km_petronad.fluids', required=True)
    plan = fields.Integer(required=True)
    description = fields.Text( )


    @api.model
    def create(self, vals):
        res = super(KmPetronadProductionPlan, self).create(vals)

        print(f'PLAN create: {vals}')
        return res

class KmPetronadProductionUnit(models.Model):
    _name = 'km_petronad.production_unit'

    name = fields.Char( required=True)
    company = fields.Many2one( 'res.company', required=True)
    description = fields.Text( )

class KmPetronadAnalysis(models.Model):
    _name = 'km_petronad.analysis'


    production = fields.Many2one( 'km_petronad.production_record', required=True)
    fluid = fields.Many2one('km_petronad.fluids', required=True)
    water = fields.Float()

    # PEG off
    m = fields.Float()
    d = fields.Float()
    t = fields.Float()
    tt = fields.Float()
    salt = fields.Float()
    uk = fields.Float()

    # Glycerin crude
    nacl = fields.Float()
    glycerin = fields.Float()
    mong = fields.Float()
    methanol = fields.Float()
    ph = fields.Float()
