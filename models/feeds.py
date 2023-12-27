# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime
import jdatetime
import json


class KmPetronadFeeds(models.Model):
    _name = 'km_petronad.feeds'
    _order = 'project,feed_date'

    feed_date = fields.Date(default=lambda self: date.today(), required=True )
    project = fields.Many2one('project.project', )
    feed_amount = fields.Integer()
    feed_analysis = fields.Float()
    contractor = fields.Many2one('res.partner')
    transport = fields.Integer()
    description = fields.Text()


