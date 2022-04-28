#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
API of User management
"""

from typing import List, Any

from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from starlette.responses import Response

from models.user import User as UserDAO, verify_user_password
from schemas.user import UserOut, UserIn, UserUpdate, PasswordChange
from tools.auth import get_current_user
from tools.crypto import generate_salt, hash_password
from tools.db import get_db

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

user_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="This user doesn't exist")


@router.get('/', response_model=List[UserOut], dependencies=[Depends(get_db)])
def list_user() -> List[UserOut]:
    """
    List all user
    """
    return list(UserDAO.select())


def replace_secrets(payload: dict[str, Any]):
    """
    Replace password with its hash when updating or creating a user.
    :param payload: the dict of the input
    """
    if payload['password'] != "":
        payload['password'] = hash_password(payload['password'],
                                            generate_salt())


@router.post('/', response_model=UserOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_db)])
def create_user(body: UserIn) -> UserOut:
    """
    Create a new user
    """
    payload = body.dict()
    if UserDAO.get_or_none(username=payload['username']) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An user with the same username already exists")
    if UserDAO.get_or_none(email=payload['email']) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An user with the same e-mail address already exists")

    replace_secrets(payload)

    user_obj = UserDAO(**payload)
    user_obj.save()
    return user_obj


@router.get('/{user_id}', response_model=UserOut, dependencies=[Depends(get_db)])
def get_user(user_id: int) -> UserOut:
    """
    Get a user given its identifier
    """
    try:
        user = UserDAO.get(UserDAO.id == user_id)
    except UserDAO.DoesNotExist:
        raise user_not_found
    return user


@router.get('/me/', response_model=UserOut, dependencies=[Depends(get_db)])
def get_logged_user(login_info: tuple[UserDAO, List[str]] = Depends(get_current_user)) -> UserOut:
    """
    Get the connected user
    """
    return login_info[0]


@router.put('/me/', response_model=UserOut, dependencies=[Depends(get_db)])
def update_user(body: UserUpdate, login_info: tuple[UserDAO, List[str]] = Depends(get_current_user)) -> UserOut:
    """
    Update the connected user
    """
    user, _ = login_info
    payload = body.dict(exclude_unset=True)
    if UserDAO.get_or_none(username=payload['username']) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An user with the same username already exists")
    if UserDAO.get_or_none(email=payload['email']) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An user with the same e-mail address already exists")

    replace_secrets(payload)
    user.update(**payload)
    return user


@router.put('/me/password', status_code=status.HTTP_204_NO_CONTENT)
def update_user_password(body: PasswordChange,
                         login_info: tuple[UserDAO, List[str]] = Depends(get_current_user)) -> Response:
    """
    Update a user password given its identifier
    """
    payload = body.dict(exclude_unset=True)
    replace_secrets(payload)
    if not verify_user_password(login_info[0], payload['old_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong password",
        )
    login_info[0].password = payload['password']
    login_info[0].save()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_db)])
def delete_user(user_id: int) -> Response:
    """
    Delete a user given its identifier
    """
    try:
        UserDAO[user_id].delete_instance()
    except UserDAO.DoesNotExist:
        raise user_not_found
    return Response(status_code=status.HTTP_204_NO_CONTENT)
