from app.routers.actions import delete_action_ressource_file
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from tortoise.transactions import atomic

from app.models.action import Action
from app.models.activity import (Activity, ActivityIn, ActivityInPatch,
                                 ActivityOut, ActivityText)
from app.models.artifact import Artifact
from app.models.language import Language
from app.types.response import IDResponse
from app.utils import insctructor_required

router = APIRouter()


@router.get("/{activity_id}")
async def get_activity(activity_id: int, language_code: str = 'fr'):
    """ Get an action"""
    activity_text = await ActivityText.get(activity_id=activity_id, language__code=language_code).prefetch_related("language", "activity__artifacts")
    return ActivityOut(
        id=activity_text.activity.id,
        name=activity_text.name,
        description=activity_text.description,
        language=activity_text.language.code,
        start=activity_text.activity.start_id,
        artifacts=[artifact.id for artifact in activity_text.activity.artifacts],
    )


@router.post("/", response_model=IDResponse)
@atomic()
async def create_activity(activity: ActivityIn, _=Depends(insctructor_required)):
    """ Create an action """
    activity_db = await Activity.create(
        start_id=activity.start,
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


@router.patch("/{activity_id}", response_model=ActivityOut)
@atomic()
async def update_activity(activity_id: int, activity: ActivityInPatch, language_code: str = "fr", _=Depends(insctructor_required)):
    """ Update an action without specifying all the fields """
    activity_db = await Activity.get(id=activity_id)
    activity_text, created = await ActivityText.get_or_create(activity=activity_db,
                                                              language_id=(await Language.get(code=language_code)).id,
                                                              defaults={"name": "", "description": ""})
    if created and (activity.name is None or activity.description is None):
        raise HTTPException(status_code=400, detail="You must specify a name and a description for the activity when adding a new language")
    if "name" in activity.__fields_set__:
        activity_text.name = activity.name
    if "description" in activity.__fields_set__:
        activity_text.description = activity.description
    if "start" in activity.__fields_set__:
        activity_db.start_id = activity.start
    if "artifacts" in activity.__fields_set__:
        await activity_db.artifacts.clear()
        artifacts_to_add = await Artifact.filter(id__in=activity.artifacts if activity.artifacts is not None else [])
        await activity_db.artifacts.add(*artifacts_to_add)
    await activity_db.save()
    await activity_text.save()
    return await get_activity(activity_id, language_code)


@router.delete("/{activity_id}", response_model=IDResponse)
@atomic()
async def delete_activity(activity_id: int, _=Depends(insctructor_required)):
    """ Delete an action """
    activity = await Activity.get(id=activity_id).prefetch_related("texts")
    await activity.texts.all().delete()
    if activity.start_id is not None:
        await delete_action_by_right(activity.start_id)
    await activity.delete()
    return IDResponse(id=activity_id)


async def delete_action_by_right(action_id: int):
    """ Delete an action by right """
    action = await Action.get(id=action_id)
    await delete_action_ressource_file(action)
    await action.delete()
    if action.next_id is not None:
        await delete_action_by_right(action.next_id)