# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
import jdatetime
import json


class KmPetronadComments(models.Model):
    _name = 'km_petronad.comments'

    comment_date = fields.Date(default=lambda self: datetime.now().date() - timedelta(hours=3.5), required=True)
    description = fields.Html()

