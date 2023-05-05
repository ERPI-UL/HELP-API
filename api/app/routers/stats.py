import tortoise
from fastapi import APIRouter, Depends
from app.types.stat import ScenarioStats, StepStat
from app.utils import get_current_user_in_token

router = APIRouter()

@router.get('/activities/{id_activity}', response_model=ScenarioStats)
async def get_scenario_stats(id_activity: int, _=Depends(get_current_user_in_token)):
    pass