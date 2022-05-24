import base64
from datetime import datetime, timedelta
import random
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import utils
import Models
import jwt
import mail
router = APIRouter()


@router.post('/token', tags=["auth"])
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await utils.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utiliateur ou mot de passe incorrect"
        )
    user_obj = await Models.UserinToken.from_tortoise_orm(user)
    token = jwt.encode(user_obj.dict(), utils.JWT_SECRET)
    return {'access_token': token, 'token_type': 'bearer'}


@router.post("/password", tags=["auth"])
async def change_password(data: Models.PasswordChange):
    user = await utils.authenticate_user(data.username, data.old)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utiliateur ou mot de passe incorrect"
        )
    user.password_hash = Models.User.encrypt_password(data.new)
    await user.save()
    return {'ok'}


@router.post("/reset", tags=["auth"])
async def reset_password(data: Models.PasswordReset):
    reset = await Models.Reset.get_or_none(token=data.token).prefetch_related('user').first()
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
    reset.user.password_hash = Models.User.encrypt_password(data.password)
    await reset.user.save()
    await reset.delete()
    return {'ok'}


@router.get("/reset/{userORemail}", tags=["auth"])
async def reset_password_get(userORemail: str):
    token = base64.b16encode(random.getrandbits(
        256).to_bytes(32, byteorder='little')).decode('utf-8')
    user:Models.User = await Models.User.filter(username=userORemail,email=userORemail).first()
    dateExpiration = datetime.now() + timedelta(hours=1)
    reset = Models.Reset(user=user, token=token, expiration=dateExpiration)
    await reset.save()
    await mail.sendResetLink(user.email,token,user.firstname,user.lastname)
    return {'message': 'Un email vous a été envoyé pour réinitialiser votre mot de passe'}
