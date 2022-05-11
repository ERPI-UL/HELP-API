
import random
from fastapi import APIRouter
import utils
import Models
from fastapi import Depends, HTTPException, status
import asyncio
from datetime import datetime, timedelta
router = APIRouter()

#dictionnaire de code et de token
easyAuth = {}

def getEasyCode():
    """
    Génère un code aléatoire de 5 caractères en vérifiant qu'il n'est pas déjà utilisé
    Returns:
        code (str): code aléatoire de 5 caractères
    """
    run = True
    while(run):
        x = ''.join(random.choices('123456789', k=5))
        run = x in easyAuth
    # expires in 10 minutes
    easyAuth[x] = {}
    easyAuth[x]['expires'] = datetime.now() + timedelta(minutes=10)
    easyAuth[x]['token'] = 'tokenbidon'
    print(easyAuth)
    print(type(easyAuth))
    return x


@router.post("/connect")
async def easy_login(code: Models.Easy, current_user: Models.User = Depends(utils.get_current_user_in_token)):
    if not code.token:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Token manquant"
        )
    if code.code not in easyAuth:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Code appareil invalide",
        )
    easyAuth[code.code]['token'] = code.token
    return {'ok'}


@router.get("/generate")
async def get_easy_code():
    return {'code': getEasyCode()}


@router.get("/{code}")
async def getToken(code: str):
    run = True
    while(run):
        if easyAuth[code]['token'] != 'tokenbidon':
            run = False
        await asyncio.sleep(1)
    return {'token': easyAuth[code]['token']}
