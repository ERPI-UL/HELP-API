import os
from enum import Enum

import jwt
import tortoise
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from passlib.hash import bcrypt
from pydantic import BaseModel

from app.customScheme import CustomOAuth2PasswordBearer
from app.models import User, UserinFront, UserinToken

load_dotenv()

JWT_SECRET = os.getenv('SECRET_KEY')
DB_URL = os.getenv('DB_HOST')
DATA_DIRECTORY = './app/data/'
MODELS_DIRECTORY = DATA_DIRECTORY+'models/'
SCENARIOS_DATA_DIRECTORY = DATA_DIRECTORY+'scenarios/'
oauth2_scheme = CustomOAuth2PasswordBearer(tokenUrl='auth/token')


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """ Return the user if the token is correct"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await User.get(id=payload.get('id'))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utiliateur ou mot de passe incorrect"
        ) from exc

    return await UserinFront.from_tortoise_orm(user)


async def get_current_user_in_token(token: str = Depends(oauth2_scheme)):
    """ Return the user if the token is correct"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = UserinToken(id=payload.get('id'), username=payload.get(
            'username'), adminLevel=payload.get('adminLevel'))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide"
        ) from exc

    return user


async def get_token(token: str = Depends(oauth2_scheme)):
    """ Return the token if it is correct"""
    try:
        jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide"
        ) from exc
    return token


async def get_admin_level(user: UserinFront = Depends(get_current_user)) -> int:
    """ Return the admin level of the user"""
    return user.adminLevel


async def is_admin(user: UserinFront = Depends(get_current_user)) -> bool:
    """ Return True if the user is an admin"""
    return user.adminLevel == Permission.ADMIN.value


async def admin_required(user: bool = Depends(is_admin)):
    """ Raise an exception if the user is not an admin"""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'avez pas les droits nécessaires"
        )


async def is_instructor_or_above(user: UserinFront = Depends(get_current_user_in_token)):
    """ Return the user if the user is an instructor or an admin"""
    return user.adminLevel >= Permission.INSTRUCTOR.value


async def is_himself(id_user: int, user: UserinFront = Depends(get_current_user_in_token)):
    """ Raise an exception if the user is not the same as the one in the token"""
    if user.id != id_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Vous n'avez pas le droit de faire cette action"
        )


async def insctructor_required(user: UserinFront = Depends(is_instructor_or_above)):
    """ Raise an exception if the user is not an instructor"""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'avez pas les droits suffisants"
        )
    return user


async def authenticate_user(username: str, password: str):
    """ Return the user if the username and password are correct"""
    user = await User.get(username=username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


async def init_admin():
    """ Create the admin user if it doesn't exist"""
    try:
        user = await User.get(username='toxicbloud')
        if not user:
            user = await User.create(username='toxicbloud', email='truc@gmail.com',
                                     adminLevel=Permission.ADMIN.value, password_hash=bcrypt.hash(JWT_SECRET),
                                     firstname='Antonin', lastname='Rousseau')
        else:
            user.adminLevel = Permission.ADMIN.value
            await user.save()
    except tortoise.exceptions.DoesNotExist:
        user = await User.create(username='toxicbloud', email='truc@gmail.com',
                                 adminLevel=Permission.ADMIN.value, password_hash=bcrypt.hash(JWT_SECRET),
                                 firstname='Antonin', lastname='Rousseau')


def htmlspecialchars(html):
    """ Sanitize a string to be used in html"""
    return html.replace("<", " ")\
        .replace(">", " ")\
        .replace('"', " ")\
        .replace("'", " ")\

# sanitize string to be used in html in a pydantic model


def sanitizer(obj):
    """ Sanitize a string or a list of string or a dict of string or a pydantic model"""
    if isinstance(obj, str):
        return htmlspecialchars(obj)
    elif isinstance(obj, list):
        return [sanitizer(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: sanitizer(v) for k, v in obj.items()}
    elif isinstance(obj, BaseModel):
        for attr in obj.dict():
            setattr(obj, attr, sanitizer(getattr(obj, attr)))
        return obj
    else:
        return obj


class Permission(Enum):
    """ Enum for the permission level of a user"""
    VISITOR = 0
    APPRENTICE = 1
    INSTRUCTOR = 2
    ADMIN = 3
