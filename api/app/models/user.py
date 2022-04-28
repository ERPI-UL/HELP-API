#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Definition of User model and tools associated
"""

from datetime import datetime

import peewee as pw

from tools.crypto import verify_password
from tools.db import db


class User(pw.Model):
    """user object"""
    id = pw.AutoField()
    username = pw.CharField(null=True, unique=True)
    password = pw.CharField(null=True)
    first_name = pw.CharField()
    name = pw.CharField()
    role = pw.CharField()
    email = pw.CharField(null=True, unique=True)
    last_login = pw.DateTimeField(null=True)

    created_at = pw.DateTimeField(default=datetime.utcnow)
    updated_at = pw.DateTimeField(default=datetime.utcnow)

    class Meta:
        database = db


def verify_user_password(user: User, password: str) -> bool:
    """Verify if the given password correspond to the User"""
    return verify_password(user.password, password)


def update_last_login(user: User):
    """Update last login date for a given user"""
    user.last_login = str(datetime.today())
    user.save()
