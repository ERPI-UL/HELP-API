#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Definition of submission model of a campaign and tools associated
"""
import datetime

import peewee as pw
from playhouse.postgres_ext import BinaryJSONField

from models.user import User
from models.campaign_node import CampaignNode
from tools.db import db


class Submission(pw.Model):
    """Submission object"""
    id = pw.AutoField()
    node = pw.ForeignKeyField(CampaignNode, backref="permissions")
    submitter = pw.ForeignKeyField(User, backref="permissions")
    data = BinaryJSONField()
    is_complete = pw.BooleanField(default=False)
    created_at = pw.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = pw.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        database = db
