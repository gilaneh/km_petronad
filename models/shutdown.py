# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime
import jdatetime
import json


class KmPetronadShutdown(models.Model):
    _name = 'km_petronad.shutdown'

    shutdown_date = fields.Date(default=lambda self: date.today())
    shutdown_time = fields.Integer()
    project = fields.Many2one('project.project', )
    shutdown_type = fields.Many2one('km_petronad.shutdown_type')
    description = fields.Text()


class KmPetronadShutdownType(models.Model):
    _name = 'km_petronad.shutdown_type'

    name = fields.Char(require=True)
