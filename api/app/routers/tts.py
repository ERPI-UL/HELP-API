from enum import Enum
import random
import aiohttp
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status, Response
from fastapi.responses import FileResponse
from aiogtts import aiogTTS
from aiofiles import os
from starlette.background import BackgroundTasks
import Models
import utils
router = APIRouter()

session = aiohttp.ClientSession(
    headers={"Content-Type": "text/plain;charset=UTF-8"})


class Languages(dict, Enum):
    FRENCH = {'name': 'fr-FR', 'voice': 'fr-FR-Wavenet-C'}
    ENGLISH = {'name': 'en-US', 'voice': 'en-US-Wavenet-F'}
    ESPANOL = {'name': 'es-ES', 'voice': 'es-ES-Wavenet-C'}
    GERMAN = {'name': 'de-DE', 'voice': 'de-DE-Wavenet-F'}

# @router.post("/")
# async def tts(language: str, text: str):
#     try:
#         async with session.post('https://cxl-services.appspot.com/proxy?url=https://texttospeech.googleapis.com/v1beta1/text:synthesize&token=03AGdBq248o4YrJwtLFc4PTxjOBj4gYUsUV-TSWGhYcJs3E75NlOrbNUkWEQnUBpr9iZ8ihl7xXrkjYkw-XACD6f9ZiyDOpL_rD-pe54RCgSuhN4TcJ7kedxzA8i3Wa0uB9xSVL_MM8P87xkZwP_AGEoBEt_E_kKFPnOyvIQvQBWB-eoCnw9GBUFrzjgFPcJIslRKa9bpGu1RPKUkZeItmfA8ZBxqbSComoWc6yyoQyc-Mchvnlh4Y16whuXva4gSlsMmF_xAYzMtLA92FuEv55Zd5mIXg4F7HYFUMkZVD9EkAytb4m5XoWTAQqn25vJLWKYTCuN5MABuJNpaUwc-P0cUTDA_Vq3I5Kwt23LIwBbV8lAl0mrCB7yYlRwG4xQ0PMN8kgImlxIAQ_0amoNWNUGhWfKk-vGprJ7HyTV2Cmfuqbp7gOHfzCI174AcZBfbGXPYVP5BKtIDicOXMmcE2jtNiK166C3J3cw',
#                      data={"input": {"text": "Bonjour, je m'appelle Céline, je suis votre assistante vocale. Je vous ai bien le plaisir de me voir. Je vous souhaite une bonne journée.", "voice": {"languageCode": Languages[language]["name"], "name": Languages[language]["voice"]}, "audioConfig": {"audioEncoding": "LINEAR16", "pitch": 0, "speakingRate": 1.15, "effectsProfileId": ["headphone-class-device"]}}}) as response:
#             return await response.json()
#         async with session.get(f'http://worldtimeapi.org/api/timezone/Europe/Paris') as response:
#             result = await response.json()
#             return result
#     except Exception as e:


async def cleanup(filename):
    await os.remove(filename)


@router.post("/", response_class=FileResponse)
async def tts(language: str, text: str, bg_tasks: BackgroundTasks,currentUser:Models.User= Depends(utils.get_current_user_in_token)):
    # TODO: legal problem ?
    aiogtts = aiogTTS()
    filename = 'temp'+str(random.randint(10, 100000000))+'.mp3'
    await aiogtts.save(text, filename, lang=language)
    bg_tasks.add_task(cleanup, filename)
    return FileResponse(filename, media_type='application/octet-stream', filename='res.mp3')
