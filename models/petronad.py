# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime
import jdatetime
import json


class KmPetronadPetronad(models.Model):
    _name = 'km_petronad.petronad_data'
    _order = 'project,date'

    date = fields.Date(default=lambda self: date.today() )
    project = fields.Many2one('km_petronad.projects', default=lambda self: self.env[('km_petronad.projects')].search([], limit=1))
    meg_daily = fields.Float()
    deg_daily = fields.Float()
    teg_daily = fields.Float()
    feed = fields.Float()
    output = fields.Float()

    meg_product = fields.Float()
    deg_product = fields.Float()
    teg_product = fields.Float()

    meg_total = fields.Float()
    deg_total = fields.Float()
    teg_total = fields.Float()

    total_amount = fields.Float()

    def get_data_plotly(self, project_id, start_date, end_date, chart_type='bar'):
        # print(f'========>\n {project_id}, {start_date}, {end_date}')
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        records = self.search([('project', '=', int(project_id)),
                               ('date', '>=', start_date),
                               ('date', '<=', end_date),])

        calendar = self.env.context.get('lang')

        records_date = [rec.date for rec in records]
        if calendar == 'fa_IR':
            date_format = '%Y/%m/%d'
            records_date = [jdatetime.date.fromgregorian(date=rec).strftime(date_format) for rec in records_date]
        else:
            date_format = '%Y-%m-%d'
            records_date = [rec.strftime(date_format) for rec in records_date]

        fields_list = ['feed',
                       'meg_daily', 'deg_daily', 'teg_daily',
                       'meg_product', 'deg_product', 'teg_product',
                       'meg_total', 'deg_total', 'teg_total']
        default_fields = ['feed', 'meg_daily', 'meg_product', ]
        plot_data = []
        for field in fields_list:
            field_list = [rec[field] for rec in records]
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


