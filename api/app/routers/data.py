import hashlib

import aiofiles
from aiofiles.ospath import exists as async_os_path_exists
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from tortoise.transactions import atomic

from app.models.ressource import Ressource, RessourceOut
from app.types.response import IDResponse, OKResponse
from app.utils import (ACTION_DATA_DIRECTORY, RESSOURCES_DATA_DIRECTORY,
                       Permission, get_current_user_in_token,
                       instructor_required)

router = APIRouter()


@router.get('/actions/{action_id}/ressources/{ressource_name}')
async def get_action_ressource(action_id: int, ressource_name: str):
    """ Get a ressource from a step"""
    path = f"{ACTION_DATA_DIRECTORY}/{ressource_name}"
    if not await async_os_path_exists(path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ressource {ressource_name} not found for action {action_id}")
    return FileResponse(path)


@router.get('/ressources/{ressource_id}', response_model=RessourceOut)
async def get_ressource(ressource_id: int):
    """ Get a ressource from a step"""
    ressource = await Ressource.get_or_none(id=ressource_id).prefetch_related("owner")
    return RessourceOut.from_orm(ressource)


@router.get('/ressources/{ressource_id}/file')
async def get_ressource_file(ressource_id: int):
    """ Get a ressource from a step"""
    ressource = await Ressource.get_or_none(id=ressource_id)
    if not ressource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ressource {ressource_id} not found")
    path = f"{RESSOURCES_DATA_DIRECTORY}/{ressource.path}"
    if not await async_os_path_exists(path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File {ressource.path} not found")
    return FileResponse(path)


@router.post('/ressources')
@atomic()
async def create_ressource(file: UploadFile, user=Depends(get_current_user_in_token)):
    """ Create a ressource"""
    if user.adminLevel < Permission.INSTRUCTOR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to create ressources")
    extension = file.filename.split(".")[-1]
    filename = file.filename
    if extension not in ["png", "jpg", "jpeg", "mp4", "webm", "wav", "mp3", "ogg"]:
        raise HTTPException(status_code=400, detail="Ressource format not supported")
    content = await file.read()
    # verify that the size does not exceed 4MiB
    if len(content) > 20 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Ressource size must not exceed 20MiB")
    hash_value = hashlib.sha256(content).hexdigest()
    # create the directory if it does not exist
    await aiofiles.os.makedirs(RESSOURCES_DATA_DIRECTORY, exist_ok=True)
    async with aiofiles.open(f"{RESSOURCES_DATA_DIRECTORY}{hash_value}.{extension}", "wb") as file:
        await file.write(content)
    ressource = await Ressource.create(name=filename, owner_id=user.id, path=f"{hash_value}.{extension}")
    return IDResponse(id=ressource.id)


@router.delete('/ressources/{ressource_id}')
@atomic()
async def delete_ressource(ressource_id: int, _=Depends(instructor_required)):
    """ Delete a ressource"""
    ressource = await Ressource.get_or_none(id=ressource_id)
    if not ressource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ressource {ressource_id} not found")
    path = f"{RESSOURCES_DATA_DIRECTORY}/{ressource.path}"
    if not await async_os_path_exists(path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ressource file {ressource_id} not found")
    await ressource.delete()
    # search if the file is used by another ressource
    ressources = await Ressource.filter(path=ressource.path)
    if not ressources:
        await aiofiles.os.remove(path)
    return OKResponse(ok="Ressource deleted")
