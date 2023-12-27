# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime
import jdatetime
import json


class KmDataFeeds(models.Model):
    _name = 'km_petronad.feeds'
    _order = 'project,feeds_date'

    feeds_date = fields.Date(default=lambda self: date.today(), required=True )
    project = fields.Many2one('project.project', )
    feed_in = fields.Float()
    feed_out = fields.Float()
    feed_stock = fields.Float(readonly=True)
    description = fields.Text()

    @api.onchange('feed_in', 'feed_out')
    def _feed_stock(self):
        for rec in self:
            previous_rec = self.search([('feeds_date', '<', rec.feeds_date)], order='feeds_date desc', limit=1)
            if len(previous_rec) != 1:
                feed_stock = rec.feed_in - rec.feed_out
            else:
                feed_stock = previous_rec.feed_stock + rec.feed_in - rec.feed_out
            rec.write({'feed_stock': feed_stock})

    def feed_stock_btn(self):
        self._feed_stock()
