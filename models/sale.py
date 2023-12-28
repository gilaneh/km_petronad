# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime
import jdatetime
import json


class KmPetronadSale(models.Model):
    _name = 'km_petronad.sale'
    _order = 'project,sale_date'

    sale_date = fields.Date(default=lambda self: date.today(), required=True)
    project = fields.Many2one('project.project', required=True)
    product_type = fields.Many2one('km_petronad.product_type', required=True)
    amount = fields.Integer()
    total_price = fields.Integer()
    currency = fields.Many2one('res.currency')
    buyer = fields.Many2one('res.partner')
    description = fields.Text()
