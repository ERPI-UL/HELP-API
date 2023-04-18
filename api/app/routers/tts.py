import random
from enum import Enum

from aiofiles import os
from aiogtts import aiogTTS
from fastapi import APIRouter, BackgroundTasks, Body, Depends
from fastapi.responses import FileResponse

from app.utils import get_current_user_in_token

router = APIRouter()

# session = aiohttp.ClientSession(
#     headers={"Content-Type": "text/plain;charset=UTF-8"})


class Languages(dict, Enum):
    """Enum used to define the languages available for the TTS."""
    FRENCH = {'name': 'fr-FR', 'voice': 'fr-FR-Wavenet-C'}
    ENGLISH = {'name': 'en-US', 'voice': 'en-US-Wavenet-F'}
    ESPANOL = {'name': 'es-ES', 'voice': 'es-ES-Wavenet-C'}
    GERMAN = {'name': 'de-DE', 'voice': 'de-DE-Wavenet-F'}


async def cleanup(filename):
    """function used to remove the file after the response is sent."""
    await os.remove(filename)


@router.post("/", response_class=FileResponse)
async def tts(bg_tasks: BackgroundTasks, language: str = Body(...), text: str = Body(...), _=Depends(get_current_user_in_token)):
    """Route used to generate a TTS file."""
    # TODO: legal problem ?
    aiogtts = aiogTTS()
    filename = 'temp'+str(random.randint(10, 100000000))+'.mp3'
    await aiogtts.save(text, filename, lang=language)
    bg_tasks.add_task(cleanup, filename)
    return FileResponse(filename, media_type='application/octet-stream', filename='res.mp3')
