# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime
import jdatetime
import json


class KmPetronadPetronadComments(models.Model):
    _name = 'km_petronad.comments'

    date = fields.Date(default=lambda self: date.today() )
    project = fields.Many2one('project.project', )
    comment = fields.Char()
    sequence = fields.Integer(default=10)