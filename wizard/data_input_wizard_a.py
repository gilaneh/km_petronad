
# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo import Command
from colorama import Fore
from datetime import datetime, date
from datetime import timedelta
from odoo.exceptions import ValidationError, UserError
import pytz


# #############################################################################
class KmPetronadDataInputWizarda(models.TransientModel):
    _name = 'km_petronad.data_input.wizard_a'
    _description = 'Data input Wizard A'

    # todo: fix timezone
    start_datetime = fields.Datetime(required=True, default=lambda self: datetime.now().replace(hour=0, minute=0, second=0) - timedelta(hours=3.5) )
    end_datetime = fields.Datetime(required=True, default=lambda self: datetime.now().replace(hour=23, minute=59, second=59) - timedelta(hours=3.5) )
    data_date = fields.Date(required=True, default=lambda self: datetime.now() - timedelta(hours=3.5) )
    shift = fields.Selection([('day', 'Day'), ('night', 'Night')], default='day', required=True)
    shift_group = fields.Selection([('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')], default='a', required=True)
    # start_datetime = fields.Datetime(required=True,default=lambda self: datetime.now().replace(hour=0, minute=0, second=0).astimezone(pytz.timezone(self.env.context.get("tz"))).replace(tzinfo=None) )
    # end_datetime = fields.Datetime(required=True, default=lambda self: datetime.now().replace(hour=23, minute=59, second=59).astimezone(pytz.timezone(self.env.context.get("tz"))).replace(tzinfo=None) )

    # end_datetime = fields.Datetime(required=True, default=lambda self: datetime.now(pytz.timezone(self.env.context.get('tz', 'Asia/Tehran'))))
    company = fields.Many2one('res.company',)
    # production_unit = fields.Many2one('km_petronad.production_unit', default=lambda self: self.search([('company', '=', self.env.user.company_id.id)], limit=1))
    production_unit = fields.Many2one('km_petronad.production_unit', )

    feed_usage = fields.Integer()
    meg_production = fields.Integer()
    deg_production = fields.Integer()
    teg_production = fields.Integer()
    h1_production = fields.Integer()
    h2_production = fields.Integer()
    ww_production = fields.Integer()
    glycerin_production = fields.Integer()
    mpg_production = fields.Integer()

    feed_batch_number = fields.Char()
    meg_batch_number = fields.Char()
    deg_batch_number = fields.Char()
    teg_batch_number = fields.Char()
    h1_batch_number = fields.Char()
    h2_batch_number = fields.Char()
    ww_batch_number = fields.Char()
    glycerin_batch_number = fields.Char()
    mpg_batch_number = fields.Char()

    feed_tank = fields.Many2one('km_petronad.storage_tanks', default=lambda self: self.env['km_petronad.storage_tanks'].search([('fluid', '=', 'FEED')], limit=1))
    meg_tank = fields.Many2one('km_petronad.storage_tanks', default=lambda self: self.env['km_petronad.storage_tanks'].search([('fluid', '=', 'MEG')], limit=1))
    deg_tank = fields.Many2one('km_petronad.storage_tanks', default=lambda self: self.env['km_petronad.storage_tanks'].search([('fluid', '=', 'DEG')], limit=1))
    teg_tank = fields.Many2one('km_petronad.storage_tanks', default=lambda self: self.env['km_petronad.storage_tanks'].search([('fluid', '=', 'TEG')], limit=1))
    h1_tank = fields.Many2one('km_petronad.storage_tanks', default=lambda self: self.env['km_petronad.storage_tanks'].search([('fluid', '=', 'HEAVY1')], limit=1))
    h2_tank = fields.Many2one('km_petronad.storage_tanks', default=lambda self: self.env['km_petronad.storage_tanks'].search([('fluid', '=', 'HEAVY2')], limit=1))
    ww_tank = fields.Many2one('km_petronad.storage_tanks', default=lambda self: self.env['km_petronad.storage_tanks'].search([('fluid', '=', 'WW')], limit=1))
    glycerin_tank = fields.Many2one('km_petronad.storage_tanks', default=lambda self: self.env['km_petronad.storage_tanks'].search([('fluid', '=', 'GLYCERIN')], limit=1))
    mpg_tank = fields.Many2one('km_petronad.storage_tanks', default=lambda self: self.env['km_petronad.storage_tanks'].search([('fluid', '=', 'MPG')], limit=1))
    description = fields.Html()
    #
    # #############################################################################

    @api.onchange('company')
    def company_changed(self):
        self.production_unit =  self.production_unit.search([('company', '=', self.company.id)],limit=1) or False

    @api.onchange('production_unit')
    def production_unit_changed(self):
        self.fluid =  self.fluid.search([('production_units', 'in', self.production_unit.id)],limit=1) or False



    def process_data(self):
        read_form = self.read()[0]
        data = {'form_data': read_form}

        #  todo: check the capacity and residue of the tank

        if self.feed_usage > 0:
            self.check_residue(self.feed_usage, self.feed_tank)
            self.feed_tank.write({'amount': -1 * self.feed_usage + self.feed_tank.amount})
            self.write_record(self.data_date, self.feed_tank.fluid.name , self.feed_tank, self.feed_usage, self.shift, self.shift_group, 'feed_usage' )

        if self.meg_production > 0:
            self.check_capacity(self.meg_production, self.meg_tank)
            self.meg_tank.write({'amount': self.meg_production + self.meg_tank.amount})
            self.write_record(self.data_date, 'MEG', self.meg_tank, self.meg_production, self.shift, self.shift_group, 'production')
        if self.deg_production > 0:
            self.check_capacity(self.deg_production, self.deg_tank)
            self.deg_tank.write({'amount': self.deg_production + self.deg_tank.amount})
            self.write_record(self.data_date, 'DEG', self.deg_tank, self.deg_production, self.shift, self.shift_group, 'production')
        if self.teg_production > 0:
            self.check_capacity(self.teg_production, self.teg_tank)
            self.teg_tank.write({'amount': self.teg_production + self.teg_tank.amount})
            self.write_record(self.data_date, 'TEG', self.teg_tank, self.teg_production, self.shift, self.shift_group, 'production' )
        if self.h1_production > 0:
            self.check_capacity(self.h1_production, self.h1_tank)
            self.h1_tank.write({'amount': self.h1_production + self.h1_tank.amount})
            self.write_record(self.data_date, 'H1', self.h1_tank, self.h1_production, self.shift, self.shift_group, 'production' )
        if self.h2_production > 0:
            self.check_capacity(self.h2_production, self.h2_tank)
            self.h2_tank.write({'amount': self.h2_production + self.h2_tank.amount})
            self.write_record(self.data_date, 'H2', self.h2_tank, self.h2_production, self.shift, self.shift_group, 'production' )
        if self.ww_production > 0:
            self.check_capacity(self.ww_production, self.ww_tank)
            self.ww_tank.write({'amount': self.ww_production + self.ww_tank.amount})
            self.write_record(self.data_date, 'WW', self.ww_tank, self.ww_production, self.shift, self.shift_group, 'production' )
        if self.mpg_production > 0:
            self.check_capacity(self.mpg_production, self.mpg_tank)
            self.mpg_tank.write({'amount': self.mpg_production + self.mpg_tank.amount})
            self.write_record(self.data_date, 'MPG', self.mpg_tank, self.mpg_production, self.shift, self.shift_group, 'production' )
        if self.glycerin_production > 0:
            self.check_capacity(self.glycerin_production, self.glycerin_tank)
            self.glycerin_tank.write({'amount': self.glycerin_production + self.glycerin_tank.amount})
            self.write_record(self.data_date, 'GLYCERIN', self.glycerin_tank, self.glycerin_production, self.shift, self.shift_group, 'production' )

        # todo: it only works on <p><br></p>. It cannot recognize the other ones as an empty description.
        description = ''.join(list([c for c in self.description if c not in '' ]))
        if description not in ['<p><br></p>', '<p></p>','<p> </p>','<p>  </p>','<p>   </p>','<p>    </p>', ]:
            self.env['km_petronad.comments_daily'].create({
                'comment_date': self.data_date,
                'description': self.description,
                })
        # print(f'\n>>>>>>>{description}<<<<<<<<\n')


    def write_record(self, data_date, fluid, tank, amount, shift, shift_group,register_type):
        production_record = self.env['km_petronad.production_record']
        fluid_model = self.env['km_petronad.fluids']
        return production_record.create({
                                        'data_date': data_date,
                                        'fluid': fluid_model.search([('name', '=', fluid)]).id,
                                        'tank': tank.id,
                                        'amount': amount,
                                        'shift': shift,
                                        'shift_group': shift_group,
                                        'register_type': register_type,
                                    })

    def check_capacity(self, amount, tank):
        if amount > tank.capacity - tank.amount:
            raise ValidationError(_(f'The tank {tank.name} has a free capacity of {tank.capacity - tank.amount} '))

    def check_residue(self, amount, tank):
        if amount >  tank.amount:
            raise ValidationError(_(f'The tank {tank.name} residue is {tank.amount} '))


