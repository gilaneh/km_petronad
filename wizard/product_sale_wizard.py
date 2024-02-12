
# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo import Command
from colorama import Fore
from datetime import datetime, date
from datetime import timedelta
from odoo.exceptions import ValidationError, UserError
import math
import pytz
# #############################################################################
class KmPetronadProductSaleWizard(models.TransientModel):
    _name = 'km_petronad.product_sale.wizard'
    _description = 'Product Sale Wizard'

    # todo: fix timezone
    start_datetime = fields.Datetime(required=True,default=lambda self: datetime.now().replace(hour=0, minute=0, second=0) - timedelta(hours=3.5) )
    end_datetime = fields.Datetime(required=True, default=lambda self: datetime.now().replace(hour=23, minute=59, second=59) - timedelta(hours=3.5) )
    data_date = fields.Date(required=True, default=lambda self: datetime.now() - timedelta(hours=3.5) )

    # start_datetime = fields.Datetime(required=True,default=lambda self: datetime.now().replace(hour=0, minute=0, second=0).astimezone(pytz.timezone(self.env.context.get("tz"))).replace(tzinfo=None) )
    # end_datetime = fields.Datetime(required=True, default=lambda self: datetime.now().replace(hour=23, minute=59, second=59).astimezone(pytz.timezone(self.env.context.get("tz"))).replace(tzinfo=None) )

    # end_datetime = fields.Datetime(required=True, default=lambda self: datetime.now(pytz.timezone(self.env.context.get('tz', 'Asia/Tehran'))))
    company = fields.Many2one('res.company', )
    production_unit = fields.Many2one('km_petronad.production_unit', )

    amount = fields.Integer( required=True)
    fluid = fields.Many2one('km_petronad.fluids', required=True )
    tank = fields.Many2one('km_petronad.storage_tanks', )
    tank_amount = fields.Integer(related='tank.amount')
    tank_capacity = fields.Integer(related='tank.capacity')
    buyer = fields.Many2one('res.partner', required=True,  )
    transporter = fields.Many2one('res.partner', required=True )
    transport_type = fields.Selection([('tanker', 'Tanker'), ('barrel', 'Barrel')], required=True, default='tanker')
    barrel_weight = fields.Integer(default=230)
    barrel_quantity = fields.Integer(compute='_barrel_quantity')
    driver = fields.Char()
    car_plate = fields.Char()
    permit_no = fields.Char()


    # #############################################################################

    @api.onchange('company')
    def company_changed(self):
        self.production_unit =  self.production_unit.search([('company', '=', self.company.id)],limit=1) or False

    @api.onchange('production_unit')
    def production_unit_changed(self):
        self.fluid =  self.fluid.search([('production_units', 'in', self.production_unit.id)],limit=1) or False

    @api.onchange('fluid')
    def fluid_changed(self):
        self.tank =  self.tank.search([('fluid', '=', self.fluid.id)],limit=1) or False


    def process_data(self):
        read_form = self.read()[0]
        data = {'form_data': read_form}

        if self.amount > 0:
            if self.transport_type == 'tanker':
                self.check_residue(self.amount, self.tank)
                self.tank.write({'amount': -1 * self.amount + self.tank.amount})
                self.write_record()
            elif self.transport_type == 'barrel':
                self.write_record()


    def write_record(self,):
        production_record = self.env['km_petronad.production_record']
        fluid_model = self.env['km_petronad.fluids']
        return production_record.create({
                                        'data_date': self.data_date,
                                        'fluid': self.fluid.id,
                                        'tank': self.tank.id if self.transport_type == 'tanker' else False,
                                        'transport_type': self.transport_type,
                                        'barrel_quantity': self.barrel_quantity if self.transport_type == 'barrel' else 0,
                                        'barrel_weight': self.barrel_weight if self.transport_type == 'barrel' else 0,
                                        'amount': self.amount,
                                        'driver': self.driver,
                                        'car_plate': self.car_plate,
                                        'permit_no': self.permit_no,
                                        'register_type': 'sale',
                                    })

    def check_residue(self, amount, tank):
        if amount >  tank.amount:
            raise ValidationError(_(f'The tank {tank.name} residue is {tank.amount} '))

    @api.depends('amount', 'barrel_weight')
    def _barrel_quantity(self):
        self.barrel_quantity = math.ceil(self.amount / self.barrel_weight) if self.barrel_weight else 0