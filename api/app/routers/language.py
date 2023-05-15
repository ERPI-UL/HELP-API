import random
from enum import Enum
from typing import List

from aiofiles import os
from aiogtts import aiogTTS
from aiohttp import ClientSession
from fastapi import APIRouter, BackgroundTasks, Body, Depends
from fastapi.responses import FileResponse

from app.models.language import LanguageOutWithId, Language
from app.utils import get_current_user_in_token
from fastapi import HTTPException, status

router = APIRouter()


class Languages(dict, Enum):
    """Enum used to define the languages available for the TTS."""
    FRENCH = {'name': 'fr-FR', 'voice': 'fr-FR-Wavenet-C'}
    ENGLISH = {'name': 'en-US', 'voice': 'en-US-Wavenet-F'}
    SPANISH = {'name': 'es-ES', 'voice': 'es-ES-Wavenet-C'}
    GERMAN = {'name': 'de', 'voice': 'de-DE-Wavenet-F'}
    ITALIAN = {'name': 'it', 'voice': 'it-IT-Wavenet-D'}


async def cleanup(filename):
    """function used to remove the file after the response is sent."""
    await os.remove(filename)


@router.get('/', response_model=List[LanguageOutWithId], summary="Retourne toutes les langues disponibles dans l'API")
async def get_languages():
    """ Return all languages """
    return await Language.all()


@router.post("/tts", response_class=FileResponse, summary="TTS", description="Génération d'un fichier audio à partir d'un texte.")
async def tts(bg_tasks: BackgroundTasks, language: str = Body(...), text: str = Body(...), _=Depends(get_current_user_in_token)):
    """Route used to generate a TTS file."""
    # TODO: legal problem ?
    aiogtts = aiogTTS()
    filename = 'temp'+str(random.randint(10, 100000000))+'.mp3'
    if language not in Languages.__members__:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Language not found",
        )
    await aiogtts.save(text, filename, lang=Languages[language]['name'])
    bg_tasks.add_task(cleanup, filename)
    return FileResponse(filename, media_type='application/octet-stream', filename='res.mp3')


@router.post("/translate", summary="Traduction", description="Traduction de texte d'une langue à une autre.")
async def translate(source: str = Body(...), target=Body(...), text=Body(...), _=Depends(get_current_user_in_token)):
    """Route used to translate a text."""
    # TODO: switch to indico hosted service
    url = 'https://translate.argosopentech.com/translate'
    # url = "http://127.0.0.1:5000/translate"
    body = {
        'q': text,
        'source': source,
        'target': target
    }
    headers = {
        'Content-Type': 'application/json'
    }
    async with ClientSession() as session:
        async with session.post(url, json=body, headers=headers) as resp:
            if resp.status == 200:
                return (await resp.json())['translatedText']
            else:
                print(resp.text)
                print(resp.status)
                return 'Error'
