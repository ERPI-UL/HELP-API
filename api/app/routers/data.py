from aiofiles.ospath import exists as async_os_path_exists
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from app.utils import ACTION_DATA_DIRECTORY

router = APIRouter()


@router.get('/actions/{action_id}/ressources/{ressource_name}')
async def get_action_ressource(action_id: int, ressource_name: str):
    """ Get a ressource from a step"""
    path = f"{ACTION_DATA_DIRECTORY}/{ressource_name}"
    if not await async_os_path_exists(path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ressource {ressource_name} not found for action {action_id}")
    return FileResponse(path)
