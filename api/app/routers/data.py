from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from aiofiles.ospath import exists as async_os_path_exists
router = APIRouter()


@router.get('/scenarios/{scenario_id}/ressources/{ressource_name}')
async def get_ressource(scenario_id: int, ressource_name: str):
    """ Get a ressource from a step"""
    path = f'app/data/scenarios/{scenario_id}/ressources/{ressource_name}'
    if not await async_os_path_exists(path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ressource {ressource_name} not found for scenario {scenario_id}")
    return FileResponse(path)
