#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main functions for the fastAPI app
"""
import os

from fastapi import FastAPI
from filelock import FileLock

from apis import user, auth, campaign
from models import create_tables
from tools.db import db, is_sqlite

# Lock the db on table creation
db_lock = FileLock("/tmp/db.lock")


def create_app():
    """Return the FastAPI app for the user microservice"""
    app = FastAPI(
        root_path=os.environ.get('BASE_URL', default="/"),
        title='LLTK',
        version='WIP',
        description="An API for a Living Lab platform"
    )

    app.include_router(auth.router)
    app.include_router(user.router)
    app.include_router(campaign.router)

    # Locking the db with a file to ensure other workers doesn't try to create the tables at the same time
    with db_lock:
        db.connect()
        create_tables()
        if is_sqlite:
            db.pragma('foreign_keys', 1, permanent=True)
        db.close()

    secret_key = os.environ.get('SECRET_KEY', default="secretK")

    return app
