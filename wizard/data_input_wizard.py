
# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo import Command
from colorama import Fore
from datetime import datetime, date
from datetime import timedelta
from odoo.exceptions import ValidationError, UserError

# #############################################################################
class KmDataDataInputWizard(models.TransientModel):
    _name = 'km_petronad.data_input.wizard'
    _description = 'Data input Wizard'

    project = fields.Many2one('project.project', required=True, )

    data_date = fields.Date(required=True, default=lambda self: date.today())

    meg_production = fields.Float()
    deg_production = fields.Float()
    teg_production = fields.Float()
    h1_production = fields.Float()
    h2_production = fields.Float()
    description_pro = fields.Text()

    meg_sale = fields.Float()
    deg_sale = fields.Float()
    teg_sale = fields.Float()
    h1_sale = fields.Float()
    h2_sale = fields.Float()
    description_sale = fields.Text()

    feed_in = fields.Float()
    feed_out = fields.Float()
    description_feed = fields.Text()

    #
    # #############################################################################
    def process_data(self):
        read_form = self.read()[0]
        data = {'form_data': read_form}
        print(f'PROCESS:\n {read_form}')
        production_m = self.env['km_petronad.production'].create({
                'production_date': read_form.get('data_date'),
                'project': read_form.get('project')[0] if read_form.get('project') else False,
                'meg_production': read_form.get('meg_production'),
                'deg_production': read_form.get('deg_production'),
                'teg_production': read_form.get('teg_production'),
                'h1_production': read_form.get('h1_production'),
                'h2_production': read_form.get('h2_production'),
                'description': read_form.get('description_pro'),
                })
        self.env['km_petronad.feeds'].create({
                'feeds_date': read_form.get('data_date'),
                'project': read_form.get('project')[0] if read_form.get('project') else False,
                'feed_in': read_form.get('feed_in'),
                'feed_out': read_form.get('feed_out'),
                'description': read_form.get('description_feed'),
                })
        self.env['km_petronad.sale'].create({
                'sale_date': read_form.get('data_date'),
                'project': read_form.get('project')[0] if read_form.get('project') else False,
                'meg_sale': read_form.get('meg_sale'),
                'deg_sale': read_form.get('deg_sale'),
                'teg_sale': read_form.get('teg_sale'),
                'h1_sale': read_form.get('h1_sale'),
                'h2_sale': read_form.get('h2_sale'),
                'description': read_form.get('description_sale'),
                })


        # return self.env.ref('km_petronad.petronad_daily_report').report_action(self, data=data)


