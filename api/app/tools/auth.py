#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Set of function to check authorization before accessing the API.
"""

import os
from typing import Optional, List

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from models import User
from tools.crypto import generate_user_token, decode_user_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=os.environ.get('BASE_URL', default="/") + "auth/token",
                                     auto_error=False)


def login_user(user, perms):
    """Return a token for a user."""
    return generate_user_token(user.id, perms)


async def get_current_user(token: Optional[str] = Depends(oauth2_scheme)) -> tuple[User, List[str]]:
    if token is not None:
        # Checking token auth
        decoded = decode_user_token(token)
        if 'sub' not in decoded:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad token no user",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user_id = int(decoded['sub'])
        try:
            user = User.get(User.id == user_id)
        except User.DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not isinstance(decoded['aud'], str):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        permissions = decoded['aud']
        return user, permissions
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
