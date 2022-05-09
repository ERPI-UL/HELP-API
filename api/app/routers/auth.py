from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import utils
import Models
import jwt
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
    user.password = data.new
    await user.save()
    return {'ok'}
