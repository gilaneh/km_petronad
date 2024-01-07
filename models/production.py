# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime
import jdatetime
import json


class KmPetronadProduction(models.Model):
    _name = 'km_petronad.production'
    _order = 'production_date'

    # todo: make sure there is only one record for each day.
    #   visualization calculates based on this assumption.

    production_date = fields.Date(default=lambda self: date.today() )
    project = fields.Many2one('project.project', )
    meg_production = fields.Float()
    deg_production = fields.Float()
    teg_production = fields.Float()
    h1_production = fields.Float()
    h2_production = fields.Float()
    ww_production = fields.Float()
    feed = fields.Float()
    workers = fields.Integer()
    description = fields.Text()



    def get_data_plotly(self, project_id, start_date, end_date, chart_type='bar'):
        print(f'========>\n {project_id}, {start_date}, {end_date}')
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        if type(project_id) is str or type(project_id) is int:
            project_id = int(project_id)
        elif type(project_id) is dict:
            project_id = project_id.get('data').get('id')
        else:
            print(f'--------------\n {type(project_id)}')
            return

        records = self.search([('project', '=', project_id),
                               ('production_date', '>=', start_date),
                               ('production_date', '<=', end_date),])
        feed_records = self.env['km_petronad.feeds'].search([('project', '=', project_id),
                               ('feed_date', '>=', start_date),
                               ('feed_date', '<=', end_date),])

        calendar = self.env.context.get('lang')

        records_date = [rec.production_date for rec in records]
        if calendar == 'fa_IR':
            date_format = '%Y/%m/%d'
            records_date = [jdatetime.date.fromgregorian(date=rec).strftime(date_format) for rec in records_date]
        else:
            date_format = '%Y-%m-%d'
            records_date = [rec.strftime(date_format) for rec in records_date]

        fields_list = ['meg_production',
                       'deg_production', 'teg_production', 'h1_production', 'h2_production',]
        default_fields = [ 'meg_production', ]

        plot_data = []
        for field in fields_list:
            field_list = [rec[field] for rec in records ]
            plot_data.append({
                            "x": records_date,
                            "y": field_list,
                            "name": field,
                            "type": chart_type,
                            "visible": 'legendonly' if field not in default_fields else True
                            })
        fields_list = ['feed_in', 'feed_out',  ]
        default_fields = ['feed_in', ]
        for field in fields_list:
            field_list = [rec[field] for rec in feed_records ]
            plot_data.append({
                            "x": records_date,
                            "y": field_list,
                            "name": field,
                            "type": chart_type,
                            "visible": 'legendonly' if field not in default_fields else True
                            })

        plot_layout = {

        }

        return json.dumps({'plot_data': plot_data, 'plot_layout': plot_layout})

class KmPetronadProductions(models.Model):
    _name = 'km_petronad.productions'
    _order = 'production_date'

    production_date = fields.Date(default=lambda self: date.today() )
    project = fields.Many2one('project.project', )
    product_type = fields.Many2one('km_petronad.product_type', )
    amount = fields.Integer()
    product_sale = fields.Selection([('production', 'Production'), ('sale', 'Sale')],
                                    default='production', require=True)
    storage_tank = fields.Many2one('km_petronad.storage_tanks', require=True )
    description = fields.Text()

class KmPetronadProductType(models.Model):
    _name = 'km_petronad.product_type'

    name = fields.Char()