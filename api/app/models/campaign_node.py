#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Definition of a campaign node and tools associated
"""
from datetime import datetime

import peewee as pw
from playhouse.postgres_ext import BinaryJSONField

from tools.db import db


class CampaignNode(pw.Model):
    """CampaignNode object"""
    id = pw.AutoField()
    parent = pw.ForeignKeyField('self', backref="children", null=True)
    data = BinaryJSONField()

    can_submit = pw.BooleanField(default=False)
    can_submit_more_than_once = pw.BooleanField(default=False)
    must_be_submitted = pw.BooleanField(default=True)

    everyone_can_see = pw.BooleanField(default=True)
    everyone_can_submit = pw.BooleanField(default=True)
    is_hidden = pw.BooleanField(default=False)

    created_at = pw.DateTimeField(default=datetime.utcnow)

    class Meta:
        database = db
