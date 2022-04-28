#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Definition of permissions of a campaign model and tools associated
"""
import datetime

import peewee as pw

from models.user import User
from models.campaign import Campaign
from tools.db import db


class CampaignPermission(pw.Model):
    """CampaignPermission object"""
    campaign = pw.ForeignKeyField(Campaign, backref="campaign_permissions")
    user = pw.ForeignKeyField(User, backref="campaign_permissions")
    can_view = pw.BooleanField(null=True)
    can_edit = pw.BooleanField(null=True)
    created_at = pw.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = pw.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        database = db
        primary_key = pw.CompositeKey('campaign', 'user')
