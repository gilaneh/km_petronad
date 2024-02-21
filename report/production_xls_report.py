# -*- coding: utf-8 -*-
from odoo import models, fields, api , _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta
import pytz
import jdatetime
from odoo import http
import logging
import json


# ########################################################################################
class ReportKmPetronadProductionXlsReport(models.AbstractModel):
    _name = 'report.km_petronad.production_xls_report_template'
    _inherit = 'report.report_xlsx.abstract'


    # ########################################################################################
    def generate_xlsx_report(self, workbook, data, p):
        report = self.env['report.km_petronad.production_report_template']
        self.create_excel(workbook, report.get_report_values([], data))

    # ########################################################################################
    def create_excel(self, workbook, report_data ):
        if report_data.get('errors'):
            raise ValidationError(report_data['errors'])
#         print(f'''
#             report_data: {report_data}
# ''')
        sheet = workbook.add_worksheet(f'گزارش')
        bold = workbook.add_format({'bold': True})
        center = workbook.add_format({'align': 'center'})
        right = workbook.add_format({'align': 'right'})
        bold_center_bg = workbook.add_format({'bold': True,
                                           'size': 12,
                                           'align': 'center',
                                           'bg_color': '#bbbbbb',
                                           })
        warning_bg = workbook.add_format({'bold': True,
                                           'bg_color': '#ffac00',
                                           })
        bold_center = workbook.add_format({'bold': True,
                                           'align': 'center',
                                           })
        format_left_to_right = workbook.add_format({"reading_order": 1})
        format_right_to_left = workbook.add_format({"reading_order": 2})
        num_format_3 = workbook.add_format({"num_format": '0.000'})
        num_format_3_bold = workbook.add_format({"num_format": '0.000','bold': True,})
        num_format_4 = workbook.add_format({"num_format": '0.0000'})
        num_format_4_bold = workbook.add_format({"num_format": '0.0000','bold': True,})
        sheet.set_column('A:Z', 15)
        # sheet.right_to_left()
        row = iter(list(range(10000)))
        col = 0
        sheet.write(next(row), col + 1, report_data['report_name'], bold)
        # sheet.write(next(row), col + 1, report_data['report_date_show'], bold)
        next(row)
        row_no = next(row)
        sheet.write(row_no, col, 'Date', bold_center_bg)
        sheet.write(row_no, col + 1, 'Product Name', bold_center_bg)
        sheet.write(row_no, col + 2, 'Product Actual QTY', bold_center_bg)
        sheet.write(row_no, col + 3, 'Unit', bold_center_bg)
        sheet.write(row_no, col + 4, 'Tank Name', bold_center_bg)
        sheet.write(row_no, col + 5, 'Shift Time', bold_center_bg)
        sheet.write(row_no, col + 6, 'Shift Group', bold_center_bg)
        row_no = next(row)
        for data in report_data['data_records']:
            sheet.write(row_no, col + 0, data['data_date'], )
            sheet.write(row_no, col + 1, data['rec'].fluid.name or '', )
            sheet.write(row_no, col + 2, data['rec'].amount or '', )
            sheet.write(row_no, col + 3, data['rec'].unit or '', )
            sheet.write(row_no, col + 4, data['rec'].tank.name or '', )
            sheet.write(row_no, col + 5, data['rec'].shift or '', )
            sheet.write(row_no, col + 6, data['rec'].shift_group or '', )
            # print(f'{row_no}  ', end='')
            # Note: 5000 lines for row limitation
            row_no = next(row)

        row_no = next(row)


