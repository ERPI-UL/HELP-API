
import asyncio
import random
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status

from app.types.easy import Easy
from app.utils import get_current_user_in_token

router = APIRouter()

# dictionnaire de code et de token
easyAuth = {}


def get_easy_code():
    """
    Génère un code aléatoire de 5 caractères en vérifiant qu'il n'est pas déjà utilisé
    Returns:
        code (str): code aléatoire de 5 caractères
    """
    run = True
    while run:
        code = ''.join(random.choices('123456789', k=5))
        run = code in easyAuth
    # expires in 10 minutes
    easyAuth[code] = {}
    easyAuth[code]['expires'] = datetime.now() + timedelta(minutes=10)
    easyAuth[code]['token'] = 'tokenbidon'
    return code


async def remove_expired():
    """
    Supprime les codes expirés
    """
    # on créé une copie de la liste pour ne pas
    # modifier la liste originale cette opération
    # est en concurencence avec d'autres opérations
    for key in list(easyAuth):
        if easyAuth[key]['expires'] < datetime.now():
            del easyAuth[key]


@router.post("/connect")
async def easy_login(code: Easy, _=Depends(get_current_user_in_token)):
    """ Connecte un appareil à un compte utilisateur en attribuant un token a un code"""
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
async def generate_easy_code():
    """ Génère un code aléatoire de 5 caractères et le retourne """
    await remove_expired()
    return {'code': get_easy_code()}


@router.get("/{code}")
async def get_token(code: str):
    """ Retourne le token associé au code """
    if code not in easyAuth:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Code appareil invalide",
        )
    run = True
    while run:
        if easyAuth[code]['token'] != 'tokenbidon':
            run = False
        await asyncio.sleep(1)
        token = easyAuth[code]['token']
        # delete code
        del easyAuth[code]
    return {'token': token}
