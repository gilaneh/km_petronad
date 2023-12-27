# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime
import jdatetime
import json
    
class KmPetronadStorage(models.Model):
    _name = 'km_petronad.storage'
    _order = 'storage_date'

    storage_date = fields.Date(default=lambda self: date.today() )
    project = fields.Many2one('project.project', )
    meg_storage = fields.Float()
    deg_storage = fields.Float()
    teg_storage = fields.Float()
    h1_storage = fields.Float()
    h2_storage = fields.Float()
    ww_storage = fields.Float()
    feed_storage = fields.Float()
    description = fields.Text()

