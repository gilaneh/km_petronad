# -*- coding: utf-8 -*-
from odoo import models, fields, api , _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta
import pytz
import jdatetime


# ########################################################################################
class Report(models.AbstractModel):
    _name = 'report.km_petronad.daily_report_template'
    _description = 'Cargo Document'

    # ########################################################################################
    @api.model
    def _get_report_values(self, docids, data=None):

        errors = []
        doc_data_list = []
        doc_data = []
        date_format = '%Y-%m-%d'
        context = self.env.context
        time_z = pytz.timezone(context.get('tz'))
        date_time = datetime.now(time_z)
        date_time = self.date_converter(date_time, context.get('lang'))
        if docids and len(docids) > 1:
            raise ValidationError(_('Please select one record only.'))

        if docids:
            data_record = self.env['km_petronad.petronad_data'].browse(docids)
            project = data_record.project.name
            project_id = data_record.project.id
            end_date = data_record.date
            calendar = context.get('lang')
        else:
            form_data = data.get('form_data')
            project = form_data.get('project')[0]
            project_id = form_data.get('project')[1]
            start_date = form_data.get('start_date')
            end_date = form_data.get('end_date')
            start_date = datetime.strptime(start_date, date_format).date()
            end_date = datetime.strptime(end_date, date_format).date()
            # data_records = self.env['km_petronad.petronad_data'].search([('date', '>=', start_date),
            #                                                           ('date', '<=', end_date)])
            calendar = form_data.get('calendar')
            feeds_data = self.env['km_petronad.feeds'].search([('project', '=', project_id),
                                                                     ('feed_date', '=', end_date),], limit=1)
            production_data = self.env['km_petronad.production'].search([('project', '=', project_id),
                                                                     ('production_date', '=', end_date),], limit=1)
            docids = [feeds_data.id]

        s_start_date = self.date_converter(end_date, context.get('lang')).get('date')
        if len(feeds_data) == 0:
            return {
                'errors': [
                    _(f'No record have found for project  {project}  on the selected date:  {s_start_date}  ')],
            }

        last_week = end_date - timedelta(days=7)
        two_week = end_date - timedelta(days=14)
        data_records = self.env['km_petronad.feeds'].search([('project', '=', project_id),
                                                                ('feed_date', '<', end_date),
                                                                 ('feed_date', '>=', two_week), ], order='feed_date desc')
        data_last_week = [rec for rec in data_records if rec.feed_date >=  last_week]
        data_two_week = [rec for rec in data_records if rec.feed_date <  last_week]
        data_last_week_d = [rec.feed_date for rec in data_records if rec.feed_date >=  last_week]
        data_two_week_d = [rec.feed_date for rec in data_records if rec.feed_date <  last_week]

        print(f'\n ==========> \n data_last_week_d: {len(data_last_week_d)} {data_last_week_d} '
              f'\n data_two_week_d: {len(data_two_week_d)} {data_two_week_d}')
        doc_data = {
            # 'data_record': data_record,
            'feeds_data': feeds_data,
            'production_data': production_data,
            'date': self.date_converter(feeds_data.feed_date, context.get('lang')).get('date'),
            # 'meg_last_week': round(sum([rec.meg_daily for rec in data_last_week]), 2),
            # 'deg_last_week': round(sum([rec.deg_daily for rec in data_last_week]), 2),
            # 'teg_last_week': round(sum([rec.teg_daily for rec in data_last_week]), 2),
            # 'meg_two_week': round(sum([rec.meg_daily for rec in data_two_week]), 2),
            # 'deg_two_week': round(sum([rec.deg_daily for rec in data_two_week]), 2),
            # 'teg_two_week': round(sum([rec.teg_daily for rec in data_two_week]), 2),

        }

        comment_records = self.env['km_petronad.comments'].search([('project', '=', project_id),
                                                                ('date', '=', end_date), ],)
        comments = [rec.comment for rec in comment_records]
        # history = _(f'Total production is from 1401/09/05 to {s_start_date} and the amount is {data_record.total_amount}')
        history = _(f'Total production is from 1401/09/05 to {s_start_date} and the amount is ')
        print('***' * 30, 'doc_data_list\n', context.get('lang'), {comment_records})
        company_id = 7
        company_logo = f'/web/image/res.partner/{company_id}/image_128/'
        return {
            'docs': feeds_data,
            'doc_ids': docids,
            'doc_data': doc_data,
            'feeds_data': feeds_data,
            'production_data': production_data,
            'doc_data_list': doc_data_list,
            'lang': context.get('lang'),
            #
            'company_id': company_id,
            'errors': errors,
            'project': project,
            'comments': comments,
            'history': history,
            }

    # ########################################################################################
    def date_converter(self, date_time, lang):
        if lang == 'fa_IR':
            date_time = jdatetime.datetime.fromgregorian(datetime=date_time)
            date_time = {'date': date_time.strftime("%Y/%m/%d"),
                  'time': date_time.strftime("%H:%M:%S")}
        else:
            date_time = {'date': date_time.strftime("%Y/%m/%d"),
                        'time': date_time.strftime("%H:%M:%S")}
        return date_time

    # ########################################################################################
    def _table_record(self, items, start_date, first_day, last_day, record_type=False):
        day = len(list([item for item in items
                        if (not record_type or item.record_type.name == record_type)
                        and item.record_date == start_date]))

        month = len(list([item for item in items
                          if (not record_type or item.record_type.name == record_type)
                          and item.record_date <= start_date
                          and item.record_date >= first_day ]))

        total = len(list([item for item in items if (not record_type or item.record_type.name == record_type)]))
        return day, month, total

    # ########################################################################################
    def _table_record_sum_of_records(self, items, start_date, first_day, last_day, record_type=False):
        day = sum(list([item.man_hours for item in items
                        if (not record_type or item.record_type.name == record_type)
                        and item.record_date == start_date]))

        month = sum(list([item.man_hours for item in items
                          if (not record_type or item.record_type.name == record_type)
                          and item.record_date <= start_date
                          and item.record_date >= first_day ]))

        total = sum(list([item.man_hours for item in items if (not record_type or item.record_type.name == record_type)]))
        day = int(round(day, 0))
        month = int(round(month, 0))
        total = int(round(total, 0))
        return day, month, total