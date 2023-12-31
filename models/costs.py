# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime
import jdatetime
import json


class KmPetronadCost(models.Model):
    _name = 'km_petronad.cost'

    cost_date = fields.Date(default=lambda self: date.today(), required=True)
    cost_amount = fields.Integer( required=True)
    project = fields.Many2one('project.project', required=True )
    cost_type = fields.Many2one('km_petronad.cost_type', required=True)
    description = fields.Text()


class KmPetronadCostType(models.Model):
    _name = 'km_petronad.cost_type'

    name = fields.Char(require=True)
