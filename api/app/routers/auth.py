import base64
import random
from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.expressions import Q

import app.mail as mail
from app.models.reset import Reset
from app.models.user import User, UserinToken
from app.types.password import PasswordChange, PasswordReset
from app.utils import JWT_SECRET, authenticate_user

router = APIRouter()


@router.post('/token', tags=["auth"])
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """ Return a JWT token for the user if the username and password are correct"""
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utiliateur ou mot de passe incorrect"
        )
    user_obj = await UserinToken.from_tortoise_orm(user)
    token = jwt.encode(user_obj.dict(), JWT_SECRET)
    return {'access_token': token, 'token_type': 'bearer'}


@router.post("/password", tags=["auth"])
async def change_password(data: PasswordChange):
    """ Change the password of the user if the old password is correct"""
    user = await authenticate_user(data.username, data.old)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utiliateur ou mot de passe incorrect"
        )
    user.password_hash = User.encrypt_password(data.new)
    await user.save()
    return {'ok'}


@router.post("/reset", tags=["auth"])
async def reset_password(data: PasswordReset):
    """ Reset the password of the user if the reset token is correct"""
    reset = await Reset.get_or_none(token=data.token).prefetch_related('user').first()
    if not reset:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide"
        )
    if datetime.now().astimezone() > reset.expiration:
        await reset.delete()  # on supprime le lien expiré
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Lien expiré"
        )
    reset.user.password_hash = User.encrypt_password(data.password)
    await reset.user.save()
    await reset.delete()
    return {'ok'}


@router.get("/reset/{user_or_email}", tags=["auth"])
async def reset_password_get(user_or_email: str):
    """ Generate a reset token and send it to the user by email"""
    token = base64.b16encode(random.getrandbits(
        256).to_bytes(32, byteorder='little')).decode('utf-8')
    user: User = await User.filter(Q(Q(username=user_or_email), Q(email=user_or_email), join_type="OR")).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur inconnu"
        )
    date_expiration = datetime.now() + timedelta(minutes=15)
    await Reset.filter(user=user).delete()
    reset = Reset(user=user, token=token, expiration=date_expiration)
    await reset.save()
    await mail.send_reset_link(user.email, token, user.firstname, user.lastname)
    return {'message': 'Un email vous a été envoyé pour réinitialiser votre mot de passe'}
