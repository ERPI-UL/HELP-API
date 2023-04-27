from fastapi.routing import APIRouter

from app.models.activity import ActivityOut, ActivityText

router = APIRouter()


@router.get("/{action_id}")
async def get_action(action_id: int, language_code: str = 'fr'):
    """ Get an action"""
    activity_text = await ActivityText.filter(action_id=action_id, language__code=language_code).prefetch_related("action__artifacts").first()
    return ActivityOut(
        id=activity_text.action.id,
        name=activity_text.name,
        description=activity_text.description,
        language=activity_text.language.code,
        start=activity_text.action.start_id,
        artifacts=[artifact.id for artifact in activity_text.action.artifacts],
    )
