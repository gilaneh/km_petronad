
# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo import Command
from colorama import Fore
from datetime import datetime, date
from datetime import timedelta
from odoo.exceptions import ValidationError, UserError

# #############################################################################
class KmPetronadDataView(models.TransientModel):
    _name = 'km_petronad.data_view.wizard'
    _description = 'Data View Wizard'

    # def _project_domain(self):
    #     partner_id = self.env.user.partner_id
    #     projects = self.env['km_petronad.project'].search(['|',
    #                                                   ('overview_managers', 'in', partner_id.id),
    #                                                   ('overview_officers', 'in', partner_id.id),])
    #     return [('id', 'in', projects.ids)]

    project = fields.Many2one('project.project', )

    start_date = fields.Date(required=True, default=lambda self: date.today() - timedelta(days=30))
    end_date = fields.Date(required=True, default=lambda self: date.today())

    #
    # #############################################################################
    def overview_daily_data_view(self):
        read_form = self.read()[0]
        data = {'form_data': read_form}

        return self.env.ref('km_petronad.petronad_daily_report').report_action(self, data=data)


