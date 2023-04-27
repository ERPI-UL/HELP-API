from fastapi import Depends
from fastapi.routing import APIRouter
from tortoise.transactions import atomic

from app.models.activity import Activity, ActivityIn, ActivityOut, ActivityText
from app.models.artifact import Artifact
from app.models.language import Language
from app.types.response import IDResponse
from app.utils import insctructor_required

router = APIRouter()


@router.get("/{activity_id}")
async def get_action(activity_id: int, language_code: str = 'fr'):
    """ Get an action"""
    activity_text = await ActivityText.get(activity_id=activity_id, language__code=language_code).prefetch_related("activity__artifacts")
    return ActivityOut(
        id=activity_text.action.id,
        name=activity_text.name,
        description=activity_text.description,
        language=activity_text.language.code,
        start=activity_text.action.start_id,
        artifacts=[artifact.id for artifact in activity_text.action.artifacts],
    )


@router.post("/", response_model=IDResponse)
@atomic()
async def create_activity(activity: ActivityIn, _=Depends(insctructor_required)):
    """ Create an action """
    activity_db = await Activity.create(
        start=activity.start,
    )
    artifacts_to_add = await Artifact.filter(id__in=activity.artifacts)
    await activity_db.artifacts.add(*artifacts_to_add)
    language = await Language.get(code=activity.language)
    await ActivityText.create(
        name=activity.name,
        description=activity.description,
        language=language,
        activity=activity_db,
    )
    return IDResponse(id=activity_db.id)
