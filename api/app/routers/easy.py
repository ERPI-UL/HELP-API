
import asyncio
from secrets import SystemRandom, token_hex

from fastapi import APIRouter, Depends, HTTPException, status

from app.types.easy import Easy, EasyCode, EasyConnect, EasyToken
from app.utils import get_current_user_in_token, get_redis

router = APIRouter()


async def get_easy_code() -> Easy:
    """
    Génère un code aléatoire de 5 caractères en vérifiant qu'il n'est pas déjà utilisé
    Returns:
        code (str): code aléatoire de 5 caractères
    """
    redis = await get_redis()
    run = True
    while run:
        code = ''.join(SystemRandom().choice('0123456789') for _ in range(5))
        run = await redis.get(code)
    # generate a 32 hex password
    password = token_hex(32)
    await redis.setex(code, 60*5, Easy(code=code, password=password).json())
    return Easy(code=code, password=password)


@router.post("/connect")
async def easy_login(code: EasyConnect, _=Depends(get_current_user_in_token)):
    """ Connecte un appareil à un compte utilisateur en attribuant un token a un code"""
    redis = await get_redis()
    if not code.token:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Token manquant"
        )
    code_bytes = await redis.get(code.code)
    if not code_bytes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Code appareil invalide",
        )
    easy = Easy.parse_raw(code_bytes)
    ttl = await redis.ttl(code.code)
    if not easy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Code appareil invalide",
        )
    easy.token = code.token
    await redis.setex(code.code, ttl, easy.json())
    return {'ok'}


@router.get("/generate", response_model=EasyCode)
async def generate_easy_code():
    """ Génère un code aléatoire de 5 caractères et le retourne """
    return await get_easy_code()


@router.get("/{code}", response_model=EasyToken)
async def get_token(code: str, password: str):
    """ Retourne le token associé au code """
    redis = await get_redis()
    code_bytes = await redis.get(code)
    if not code_bytes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Code appareil invalide",
        )
    easy = Easy.parse_raw(code_bytes)
    if easy.password != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mot de passe incorrect",
        )
    run = True
    while run:
        code_bytes = await redis.get(code)
        if not code_bytes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Code appareil invalide",
            )
        easy = Easy.parse_raw(code_bytes)
        if easy.token:
            run = False
        await asyncio.sleep(1)
    return {'token': easy.token}
