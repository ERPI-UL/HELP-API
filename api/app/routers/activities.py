from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from fastapi_pagination import Page
from fastapi_pagination.ext.tortoise import paginate
from tortoise.transactions import atomic

from app.models.action import (Action,ActionText)
from app.models.target import (Target)
from app.models.activity import (Activity, ActivityIn, ActivityInPatch,
                                 ActivityOut, ActivityOutTranslated, ActivityText)
from app.models.artifact import Artifact
from app.models.language import Language
from app.models.workplace import WorkPlace
from app.routers.actions import delete_action_ressource_file
from app.types.response import IDResponse
from app.utils import instructor_required
from app.models.type import Type

router = APIRouter()


@router.get('/', response_model=Page, responses={200: {"description": "Successful Response", "model": Page[ActivityOutTranslated]}})
async def get_activities_translated(language_code: str = 'fr'):
    """ get all actions """
    pagination = await paginate(Activity.all().prefetch_related("texts", "texts__language", "artifacts").order_by("id"))
    pagination.items = [ActivityOutTranslated(
        id=activity.id,
        name=(await get_ask_translation_or_first(activity.texts, language_code)).name,
        description=(await get_ask_translation_or_first(activity.texts, language_code)).description,
        languages=[text.language.code for text in activity.texts],
        start=activity.start_id,
        artifacts=[int(artifact.id) for artifact in activity.artifacts],
    ) for activity in pagination.items]
    return pagination


@router.get("/search", description="Search activities that are compatible with the artifacts of the selected workplace", response_model=Page,
            responses={200: {"description": "Successful Response", "model": Page[ActivityOutTranslated]}})
async def search_activities(workplace: int, language_code: str = 'fr'):
    """ Search activities that are compatible with the artifacts of the selected workplace """
    workplace = await WorkPlace.get_or_none(id=workplace).prefetch_related("instances")
    if workplace is None:
        raise HTTPException(status_code=404, detail="Workplace not found")
    pagination = await paginate(Activity.filter(artifacts__instances__workplace=workplace).distinct().prefetch_related("texts__language", "artifacts__instances__workplace").order_by("id"))
    pagination.items = [ActivityOutTranslated(
        id=activity.id,
        name=(await get_ask_translation_or_first(activity.texts, language_code)).name,
        description=(await get_ask_translation_or_first(activity.texts, language_code)).description,
        languages=[text.language.code for text in activity.texts],
        start=activity.start_id,
        artifacts=[int(artifact.id) for artifact in activity.artifacts],
    ) for activity in pagination.items]
    return pagination


async def get_ask_translation_or_first(texts, language_code: str):
    """ get the translation of an activity or the first one """
    # trouve le texte en fr sinon retourne le premier
    for text in texts:
        if text.language.code == language_code:
            return text
    return texts[0]


@router.get("/{activity_id}", response_model=ActivityOut)
async def get_activity(activity_id: int, language_code: str = None):
    """ Get an action"""
    if not language_code:
        activity_text = await ActivityText.filter(activity_id=activity_id).prefetch_related("language", "activity__artifacts").order_by("id").first()
    else:
        activity_text = await ActivityText.get_or_none(activity_id=activity_id,
                                                       language__code=language_code).prefetch_related("language", "activity__artifacts")
    if activity_text is None:
        if not await Activity.exists(id=activity_id):
            raise HTTPException(status_code=404, detail=f"Activity {activity_id} not found")
        raise HTTPException(status_code=404, detail="Activity not found in this language")
    return ActivityOut(
        id=activity_text.activity.id,
        name=activity_text.name,
        description=activity_text.description,
        language=activity_text.language.code,
        start=activity_text.activity.start_id,
        artifacts=[artifact.id for artifact in activity_text.activity.artifacts],
    )


@router.get("/{activity_id}/languages", response_model=list[str])
async def get_action_languages(activity_id: int):
    """ Get the available languages for an activity"""
    return [text.language.code for text in await ActivityText.filter(activity_id=activity_id).prefetch_related("language")]


@router.post("/", response_model=IDResponse)
@atomic()
async def create_activity(activity: ActivityIn, _=Depends(instructor_required)):
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

@router.post("/duplicate/{activity_id}", response_model=IDResponse)
@atomic()
async def duplicate_activity(activity_id: int):
    """ Duplicate an activity """
    activity_text = await ActivityText.filter(activity_id=activity_id).prefetch_related("language", "activity__artifacts").order_by("id").first()
    if not activity_text:
        if not await Activity.exists(id=activity_id):
            raise HTTPException(status_code=404, detail=f"Activity {activity_id} not found")
        raise HTTPException(status_code=404, detail="Activity not found in this language")
    activity =  activity_text.activity
    action = await (activity.start.first()).first()

    artifact_ids = []
    for artifact in activity.artifacts:
        artifact_ids.append(artifact.id)
 
    activity_db = await Activity.create(start_id=(await duplicate_action_chain(action.id)))
    artifact_to_add = await Artifact.filter(id__in=artifact_ids)
    await activity_db.artifacts.add(*artifact_to_add)
    language = await Language.get(code=activity_text.language.code)
    await ActivityText.create(
        name=activity_text.name + ' (COPY)',
        description=activity_text.description,
        language=language,
        activity=activity_db
    )
    return IDResponse(id=activity_db.id)


@router.patch("/{activity_id}", response_model=ActivityOut)
@atomic()
async def update_activity(activity_id: int, activity: ActivityInPatch, language_code: str = None, _=Depends(instructor_required)):
    """ Update an action without specifying all the fields """
    activity_db = await Activity.get(id=activity_id).prefetch_related("texts__language")
    if not language_code:
        language_code = activity_db.texts[0].language.code
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
async def delete_activity(activity_id: int, _=Depends(instructor_required)):
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

async def duplicate_action_chain(action_id, previous_id = None, id_artifact = None):
    """
    Recursively duplicates an action and its subsequent chain of actions,
    updating the `next` field to maintain the chain structure.

    Args:
        action_id (int): The ID of the action to start duplicating from.

    Returns:
        int: The ID of the first duplicated action in the chain.
    """

    action_to_duplicate = await Action.filter(id=action_id).first()

    if not action_to_duplicate:
        return None  # Handle case where action not found

    await action_to_duplicate.fetch_related('targets', 'artifact')

    if action_to_duplicate.artifact:
        id_artifact = action_to_duplicate.artifact.id

    action_db = await Action.create(
        tag=action_to_duplicate.tag,
        type=await Type.get(id=action_to_duplicate.type_id),
        artifact_id = id_artifact,
        x=action_to_duplicate.x,
        y=action_to_duplicate.y,
        z=action_to_duplicate.z,
        previous=previous_id
    )

    targets_id = []
    for target in action_to_duplicate.targets:
        targets_id.append(target.id)
    targets_to_add = await Target.filter(id__in=targets_id)
    await action_db.targets.add(*targets_to_add)

    action_text_to_duplicate = await ActionText.filter(action_id=action_to_duplicate.id).first()
    action_text_db = await ActionText.create(
        name=action_text_to_duplicate.name,
        description=action_text_to_duplicate.description,
        hint=action_text_to_duplicate.hint,
        language_id=action_text_to_duplicate.language_id,
        action_id=action_db.id
    )

    if action_to_duplicate.next_id:
        next_action_db = await duplicate_action_chain(action_to_duplicate.next_id, action_db, id_artifact)
        action_db.next = await Action.filter(id=next_action_db).first()
        await action_db.save()  # Update next field

    return action_db.id  # Return ID of the first duplicated action