from email import utils
from enum import Enum
import os
from passlib.hash import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import tortoise
import Models
from pydantic import BaseModel
load_dotenv()

JWT_SECRET = os.getenv('SECRET_KEY')
DB_URL = os.getenv('DB_HOST')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await Models.User.get(id=payload.get('id'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utiliateur ou mot de passe incorrect"
        )

    return await Models.UserinFront.from_tortoise_orm(user)


async def get_current_user_in_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = Models.UserinToken(id=payload.get('id'), username=payload.get(
            'username'), adminLevel=payload.get('adminLevel'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide"
        )

    return user


async def get_token(token: str = Depends(oauth2_scheme)):
    try:
        jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide"
        )
    return token


async def getAdminLevel(user: Models.UserinFront = Depends(get_current_user)) -> int:
    return user.adminLevel


async def isAdmin(user: Models.UserinFront = Depends(get_current_user)) -> bool:
    return user.adminLevel == Permission.ADMIN.value


async def AdminRequired(user: bool = Depends(isAdmin)):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'avez pas les droits nécessaires"
        )


async def isInstructorOrAbove(user: Models.UserinFront = Depends(get_current_user_in_token)):
    return user.adminLevel >= Permission.INSTRUCTOR.value


async def isHimself(RequestUserId: int, user: Models.UserinFront = Depends(get_current_user_in_token)):
    if user.id != RequestUserId:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Vous n'avez pas le droit de faire cette action"
        )


async def InstructorRequired(user: Models.UserinFront = Depends(isInstructorOrAbove)):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'avez pas les droits suffisants"
        )
    return user


async def authenticate_user(username: str, password: str):
    user = await Models.User.get(username=username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


async def initAdmin():
    try:
        user = await Models.User.get(username='toxicbloud')
        if not user:
            user = await Models.User.create(username='toxicbloud', email='truc@gmail.com', adminLevel=Permission.ADMIN.value, password_hash=bcrypt.hash(JWT_SECRET), firstname='Antonin', lastname='Rousseau')
        else:
            user.adminLevel = Permission.ADMIN.value
            await user.save()
    except tortoise.exceptions.DoesNotExist:
        user = await Models.User.create(username='toxicbloud', email='truc@gmail.com', adminLevel=Permission.ADMIN.value, password_hash=bcrypt.hash(JWT_SECRET), firstname='Antonin', lastname='Rousseau')

def htmlspecialchars(html):
        return html.replace("<", " ")\
            .replace(">", " ")\
            .replace('"', " ")\
            .replace("'", " ")\

#sanitize string to be used in html in a pydantic model
def sanitizer(obj):
    if isinstance(obj, str):
        return htmlspecialchars(obj)
    elif isinstance(obj, list):
        return [sanitizer(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: sanitizer(v) for k, v in obj.items()}
    elif isinstance(obj, BaseModel):
        for attr in obj.dict():
            setattr(obj,attr,sanitizer(getattr(obj,attr))) 
        return obj
    else:
        return obj
class Permission(Enum):
    VISITOR = 0
    APPRENTICE = 1
    INSTRUCTOR = 2
    ADMIN = 3
