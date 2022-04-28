#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Definition of news of a campaign model and tools associated
"""
import datetime

import peewee as pw

from models.user import User
from models.campaign import Campaign
from tools.db import db


class News(pw.Model):
    """News object"""
    id = pw.AutoField()
    campaign = pw.ForeignKeyField(Campaign, backref="news")
    author = pw.ForeignKeyField(User, backref="news")
    name = pw.CharField()
    content = pw.TextField(null=True)
    created_at = pw.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = pw.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        database = db
