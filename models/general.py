# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime
import jdatetime
import json


class KmPetronadProductType(models.Model):
    _name = 'km_petronad.product_type'

    name = fields.Char()

