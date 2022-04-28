#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
API for authentication
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from models.user import User, verify_user_password, \
    update_last_login
from tools.auth import login_user
from tools.db import get_db

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/token", dependencies=[Depends(get_db)])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login a user using its identifier.
    The time of validity can be set in config.py with TOKEN_VALIDITY_TIME.
    """
    incorrect = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        username = form_data.username
        user = User.get_or_none(User.username == username)
        if user is None:
            user = User.get(User.email == username)
    except User.DoesNotExist:
        raise incorrect

    if not verify_user_password(user, form_data.password):
        raise incorrect
    # User is now authenticated, we can proceed
    update_last_login(user)
    token = login_user(user, user.role)
    return {"access_token": token, "token_type": "bearer"}
