# -*- coding: utf-8 -*-
from odoo import models, fields, api , _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta
import pytz
import jdatetime


# ########################################################################################
class Report(models.AbstractModel):
    _name = 'report.km_petronad.production_report_template'
    _description = 'Petronad Production'

    # ########################################################################################

    def get_report_values(self, docids, data=None):
        return self._get_report_values(docids, data)

    @api.model
    def _get_report_values(self, docids, data=None):
        form_data = data.get('form_data')
        fluid_ids = form_data.get('fluids')
        fluids = self.env['km_petronad.fluids'].browse(fluid_ids)
        register_type = form_data.get('register_type')
        production_records = self.env['km_petronad.production_record'].sudo().search([
                                        ('fluid', 'in', fluid_ids),
                                        ('register_type', '=', register_type),
                                    ], order='data_date')
        calendar = self.env.context.get('lang')

        report_name = f'{register_type} : {" ".join(list([rec.name for rec in fluids]))}'
        data_records = list([
            {
                'data_date': self.date_convert(rec.data_date, calendar),
                'rec': rec,
             }
            for rec in production_records
        ])
        return {
            'report_name': report_name,
            'data_records': data_records,
        }


    def date_convert(self, date, calendar):
        if calendar == 'fa_IR':
            s_start_date = jdatetime.date.fromgregorian(date=date).strftime("%Y/%m/%d")
        else:
            s_start_date = date.strftime("%Y-%m-%d")

        return s_start_date
