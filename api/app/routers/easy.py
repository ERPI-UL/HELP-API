
import random
from fastapi import APIRouter
import utils
import Models
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
import asyncio
router = APIRouter()

easyAuth = {
    '12345': {"sid": "rehetjhnepjohn", "token": 'tokenbidon'},
}


def getEasyCode():
    run = True
    while(run):
        x = ''.join(random.choices('123456789', k=5))
        run = x in easyAuth
    easyAuth[x] = 'tokenbidon'
    return x


@router.post("/connect")
async def easy_login(code: Models.Easy):
    if not code.token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token manquant"
        )
    if code.code not in easyAuth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Code appareil invalide",
        )
    easyAuth[code.code] = code.token
    return {'ok'}


@router.get("/generate")
async def get_easy_code():
    return {'code': getEasyCode()}


@router.get("/{code}")
async def getToken(code: str):
    run = True
    while(run):
        if easyAuth[code] != 'tokenbidon':
            run = False
        await asyncio.sleep(1)
    return {'token': easyAuth[code]}


@router.delete("/{code}")
async def deleteEasy(code: str, current_user: Models.User = Depends(utils.get_current_user)):
    if easyAuth[code] != current_user.token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token incorrect"
        )
    easyAuth.pop(code)
    return {'ok'}
