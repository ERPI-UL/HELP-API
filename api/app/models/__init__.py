#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialisation of models
"""
from models.news import News
from models.campaign import Campaign
from models.campaign_perm import CampaignPermission
from models.campaign_node import CampaignNode
from models.campaign_node_perm import CampaignNodePermission
from models.submission import Submission
from models.user import User
from tools.db import db


def create_tables():
    """Create tables for all models"""
    db.create_tables([User, Campaign, News, CampaignNode, CampaignPermission, CampaignNodePermission, Submission])
