# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
import jdatetime
import json
from dateutil.relativedelta import relativedelta
from dateutil.rrule import *
TEHRAN_TIME = 3.5

class KmPetronadComments(models.Model):
    _name = 'km_petronad.comments'
    _order = 'comment_date desc'
    _rec_name = 'comment_date'

    comment_date = fields.Date(default=lambda self: datetime.now().date() - timedelta(hours=TEHRAN_TIME), required=True)
    description = fields.Html()

class KmPetronadCommentsDaily(models.Model):
    _name = 'km_petronad.comments_daily'
    _order = 'comment_date desc'
    _rec_name = 'comment_date'

    comment_date = fields.Date(default=lambda self: datetime.now().date() - timedelta(hours=TEHRAN_TIME), required=True)
    description = fields.Html()

class KmPetronadCommentsWeekly(models.Model):
    _name = 'km_petronad.comments_weekly'
    _order = 'comment_date desc'
    _rec_name = 'comment_date'

    comment_date = fields.Date(default=lambda self: datetime.now().date() - timedelta(hours=TEHRAN_TIME), required=True)
    description = fields.Html()

    @api.depends('comment_date', )
    @api.onchange('comment_date', )
    def date_chane(self):
        self.comment_date = self.comment_date + relativedelta(weekday=FR(1))



