#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Definition of permissions of a campaign model and tools associated
"""
import datetime

import peewee as pw

from models.user import User
from models.campaign_node import CampaignNode
from tools.db import db


class CampaignNodePermission(pw.Model):
    """CampaignNodePermission object"""
    node = pw.ForeignKeyField(CampaignNode, backref="permissions")
    user = pw.ForeignKeyField(User, backref="permissions")
    can_view = pw.BooleanField(null=True, default=False)
    can_submit = pw.BooleanField(null=True, default=False)
    can_see_data = pw.BooleanField(null=True, default=False)
    can_edit = pw.BooleanField(null=True, default=False)
    created_at = pw.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = pw.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        database = db
        primary_key = pw.CompositeKey('node', 'user')
