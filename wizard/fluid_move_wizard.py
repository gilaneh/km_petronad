import jdatetime

# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo import Command
from colorama import Fore
from datetime import datetime, date
from datetime import timedelta
from odoo.exceptions import ValidationError, UserError
import pytz
import math

# #############################################################################
class KmPetronadFluidMoveWizard(models.TransientModel):
    _name = 'km_petronad.fluid_move.wizard'
    _description = 'Fluid Move Wizard'

    # todo: fix timezone
    data_date = fields.Date(required=True, default=lambda self: datetime.now() - timedelta(hours=3.5) )
    tank_origin = fields.Many2one('km_petronad.storage_tanks',  )
    tank_origin_amount = fields.Integer(related='tank_origin.amount')
    tank_origin_capacity = fields.Integer(related='tank_origin.capacity')
    transfer_type = fields.Selection([('tank_to_tank', 'Tank to Tank'),
                                      ('tank_to_barrel', 'Tank to Barrel'),
                                      ('barrel_to_tank', 'Barrel to Tank')], default='tank_to_tank', required=True)
    tank_destination = fields.Many2one('km_petronad.storage_tanks',  )
    tank_destination_amount = fields.Integer(related='tank_destination.amount')
    tank_destination_capacity = fields.Integer(related='tank_destination.capacity')
    barrel_weight = fields.Integer(default=230)
    barrel_quantity = fields.Integer(compute='_barrel_quantity')
    amount = fields.Integer(required=True)
    description = fields.Html()
    #
    # #############################################################################


    def process_data(self):
        read_form = self.read()[0]
        data = {'form_data': read_form}

        if self.amount > 0 and self.transfer_type == 'tank_to_tank':
            self.check_capacity(self.amount, self.tank_origin, 'origin')
            self.check_capacity(self.amount, self.tank_destination, 'destination')
            self.tank_origin.write({'amount': -1 * self.amount + self.tank_origin.amount})
            self.tank_destination.write({'amount':  self.amount + self.tank_destination.amount})
            self.add_daily_comment(self.data_date, self.amount, self.tank_origin.name, self.tank_destination.name,)

        elif self.amount > 0 and self.transfer_type == 'tank_to_barrel':
            self.check_capacity(self.amount, self.tank_origin, 'origin')
            self.tank_origin.write({'amount': -1 * self.amount + self.tank_origin.amount})
    #         todo: create a record for barrels
            self.add_daily_comment(self.data_date, self.amount, self.tank_origin.name, f'Barrel [Q:{self.barrel_quantity} x W:{self.barrel_weight}]' )

        elif self.amount > 0 and self.transfer_type == 'barrel_to_tank':
            self.check_capacity(self.amount, self.tank_destination, 'destination')
            self.tank_destination.write({'amount': self.amount + self.tank_destination.amount})
            self.add_daily_comment(self.data_date, self.amount, f'Barrel [Q:{self.barrel_quantity} x W:{self.barrel_weight}]', self.tank_destination.name,  )

    #         todo: create a record for barrels

    @api.depends('amount', 'barrel_weight')
    def _barrel_quantity(self):
        self.barrel_quantity = math.ceil(self.amount / self.barrel_weight) if self.barrel_weight else 0


    def write_record(self, data_date, fluid, tank, amount, partner=False, analysis=0):
        production_record = self.env['km_petronad.production_record']
        fluid_model = self.env['km_petronad.fluids']
        return production_record.create({
                                        'data_date': data_date,
                                        'fluid': fluid_model.search([('name', '=', fluid)]).id,
                                        'tank': tank.id,
                                        'amount': amount,
                                        'partner': partner.id,
                                        'analysis': analysis,
                                        'register_type': 'feed_receive',
                                    })

    def check_capacity(self, amount, tank, operation):
        if operation == 'origin' and  amount > tank.amount:
            raise ValidationError(_(f'The tank {tank.name} residue is {tank.amount} '))
        if operation == 'destination' and amount > tank.capacity - tank.amount:
            raise ValidationError(_(f'The tank  {tank.name} has a free capacity of {tank.capacity - tank.amount}'))


    def add_daily_comment(self, date, amount, origin, destination,):
        jdate = jdatetime.date.fromgregorian(date=date).strftime("%Y/%m/%d")
        description = f'On {jdate} : Amount: {amount} from: {origin} to: {destination} '
        self.env['km_petronad.comments_daily'].create({
            'comment_date': date,
            'description': description,
        })
