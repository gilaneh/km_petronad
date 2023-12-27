# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime
import jdatetime
import json


class KmDataPetronadComments(models.Model):
    _name = 'km_petronad.comments'

    date = fields.Date(default=lambda self: date.today() )
    project = fields.Many2one('project.project', )
    comment = fields.Char()