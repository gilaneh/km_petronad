# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime
import jdatetime
import json

class KmPetronadTanks(models.Model):
    _name = 'km_petronad.tanks'
    _order = 'tanks_date'

    tanks_date = fields.Date(default=lambda self: date.today() )
    project = fields.Many2one('project.project', )
    meg_tank = fields.Integer()
    deg_tank = fields.Integer()
    teg_tank = fields.Integer()
    h1_tank = fields.Integer()
    h2_tank = fields.Integer()
    ww_tank = fields.Integer()
    feed_tank_1 = fields.Integer()
    feed_tank_2 = fields.Integer()
    description = fields.Text()


class KmPetronadStorageTanks(models.Model):
    _name = 'km_petronad.storage_tanks'

    name = fields.Char(require=True )
    capacity = fields.Integer(require=True)
    project = fields.Many2one('project.project', require=True )
    description = fields.Text()

