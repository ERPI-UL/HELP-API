#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Definition of Campaign model and tools associated
"""

import datetime
from typing import Optional

import peewee as pw

from models.user import User
from models.campaign_node import CampaignNode
from tools.db import db


class Campaign(pw.Model):
    """Campaign object"""
    id = pw.AutoField()
    owner = pw.ForeignKeyField(User, backref="campaigns")
    name = pw.CharField()
    description = pw.CharField(default="")
    root = pw.ForeignKeyField(CampaignNode, backref="campaign", null=True)
    is_public = pw.BooleanField(default=True)
    created_at = pw.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = pw.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        database = db

    def can_view(self, user: User) -> bool:
        """
        Return the true if the user has the right to see the campaign
        """
        from models.campaign_perm import CampaignPermission
        if self.owner == user:
            return True
        perm = CampaignPermission.get_or_none(user=user, campaign=self)
        if perm is not None and self.can_view is not None:
            if perm.can_view:
                return True
            else:
                return False
        return bool(self.is_public)

    def can_edit(self, user: User) -> bool:
        """
        Return the true if the user has the right to edit the campaign
        """
        from models.campaign_perm import CampaignPermission
        if self.owner == user:
            return True
        perm = CampaignPermission.get_or_none(user=user, campaign=self)
        if perm is None or perm.can_edit is None:
            return False
        return perm.can_edit


def get_campaign_if_available(campaign_id: int, user: User) -> Optional[Campaign]:
    """Return the campaign if it exists and if the user can see it
    """
    try:
        campaign = Campaign.get(Campaign.id == campaign_id)
    except Campaign.DoesNotExist:
        return None
    if campaign.can_view(user):
        return campaign
    return None


def get_campaign_if_editable(campaign_id: int, user: User) -> Optional[Campaign]:
    """Return the campaign if it exists and if the user can edit it
    """
    try:
        campaign = Campaign.get(Campaign.id == campaign_id)
    except Campaign.DoesNotExist:
        return None
    if campaign.can_edit(user):
        return campaign
    return None
