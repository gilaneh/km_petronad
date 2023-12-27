# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime
import jdatetime
import json


class KmPetronadSale(models.Model):
    _name = 'km_petronad.sale'
    _order = 'project,sale_date'

    sale_date = fields.Date(default=lambda self: date.today() )
    project = fields.Many2one('project.project', )
    meg_sale = fields.Float()
    deg_sale = fields.Float()
    teg_sale = fields.Float()
    h1_sale = fields.Float()
    h2_sale = fields.Float()
    description = fields.Text()
