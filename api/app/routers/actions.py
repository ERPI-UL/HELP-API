import asyncio
import hashlib

import aiofiles
from fastapi import Depends, HTTPException, UploadFile
from fastapi.routing import APIRouter
from tortoise.transactions import atomic

from app.models.action import (Action, ActionIn, ActionInPatch, ActionOut,
                               ActionText, ChoiceMember, ChoiceOut)
from app.models.language import Language
from app.models.position import PositionPost
from app.models.target import Target
from app.models.type import Type
from app.types.response import IDResponse, OKResponse
from app.utils import ACTION_DATA_DIRECTORY, instructor_required

router = APIRouter()


@router.get("/{action_id}", response_model=ActionOut)
async def get_action(action_id: int, language_code: str = None):
    """ Get an action"""
    action = await Action.get_or_none(id=action_id).prefetch_related("texts", "type", "targets")
    if action is None:
        raise HTTPException(status_code=404, detail=f"Action {action_id} not found")
    if not language_code:
        action_text = await ActionText.filter(action_id=action_id).prefetch_related("language").order_by("id").first()
    else:
        action_text = await ActionText.get_or_none(action_id=action_id,
                                                   language__code=language_code).prefetch_related("language")
    if action_text is None:
        raise HTTPException(status_code=404, detail="Action not found in this language")
    return ActionOut(
        id=action.id,
        name=action_text.name,
        description=action_text.description,
        ressource=action.ressourcePath,
        hint=action_text.hint,
        tag=action.tag,
        previous=action.previous_id,
        next=action.next_id,
        type=action.type.name,
        position=PositionPost(x=action.x, y=action.y, z=action.z),
        artifactID=action.artifact_id,
        choice=(ChoiceOut(
            left=ChoiceMember(
                target=action.left_target_action_id,
                name=action_text.left_choice
            ),
            right=ChoiceMember(
                target=action.right_target_action_id,
                name=action_text.right_choice
            )
        ) if action.type.name == "choice" else None),
        targets=[target.id for target in action.targets],
    )


@router.get("/{action_id}/languages", response_model=list[str])
async def get_action_languages(action_id: int):
    """ Get the available languages for an action"""
    return [text.language.code for text in await ActionText.filter(action_id=action_id).prefetch_related("language")]


@router.post("/", response_model=IDResponse)
@atomic()
async def create_action(action: ActionIn, _=Depends(instructor_required)):
    """ Create an action"""
    action_db = await Action.create(
        tag=action.tag,
        previous_id=action.previous,
        next_id=action.next,
        type=await Type.get(name=action.type),
        artifact_id=action.artifactID,
        x=action.position.x,
        y=action.position.y,
        z=action.position.z,
        # activity_id=action.activityID,
    )
    if not await verify_tag_unicity_in_activity(action.tag, action.previous, action.next, action_db.id):
        raise HTTPException(status_code=400, detail="Tag already used in this activity")
    if action.targets is not None:
        targets_to_add = await Target.filter(id__in=action.targets)
        await action_db.targets.add(*targets_to_add)
    await ActionText.create(
        name=action.name,
        description=action.description,
        hint=action.hint,
        language_id=(await Language.get(code=action.language)).id,
        action_id=action_db.id
    )
    return IDResponse(id=action_db.id)


@router.post("/{action_id}/ressource/", response_model=OKResponse)
async def add_ressource(action_id: int, ressource_file: UploadFile, _=Depends(instructor_required)):
    """ Add a ressource to an action"""
    action = await Action.get(id=action_id)
    extension = ressource_file.filename.split(".")[-1]
    if extension not in ["png", "jpg", "jpeg", "mp4", "webm", "wav", "mp3", "ogg"]:
        raise HTTPException(status_code=400, detail="Ressource must be an image")
    content = await ressource_file.read()
    # verify that the size does not exceed 4MiB
    if len(content) > 4 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Ressource size must not exceed 4MiB")
    hash_value = hashlib.sha256(content).hexdigest()
    # create the directory if it does not exist
    await aiofiles.os.makedirs(ACTION_DATA_DIRECTORY, exist_ok=True)
    async with aiofiles.open(f"{ACTION_DATA_DIRECTORY}{hash_value}.{extension}", "wb") as file:
        await file.write(content)
    if action.ressourcePath is not None:
        # on regarde si la ressource est utilisée par une autre action
        if await Action.filter(ressourcePath=action.ressourcePath).count() == 1 and action.ressourcePath != f"{hash_value}.{extension}":
            # si non on la supprime
            await aiofiles.os.remove(ACTION_DATA_DIRECTORY+action.ressourcePath)
    action.ressourcePath = f"{hash_value}.{extension}"
    await action.save()
    return OKResponse(ok=f"{ressource_file.filename} added to action {action_id}")


@router.delete("/{action_id}/ressource/", response_model=OKResponse)
async def delete_ressource(action_id: int, _=Depends(instructor_required)):
    """ Delete the ressource of an action"""
    action = await Action.get(id=action_id)
    if await delete_action_ressource_file(action):
        await action.save()
    else:
        raise HTTPException(status_code=400, detail="No ressource to delete")
    return OKResponse(ok=f"Ressource {action.ressourcePath} deleted from action {action_id}")


@router.patch("/{action_id}", response_model=ActionOut)
@atomic()
async def update_action(action_id: int,  action: ActionInPatch, language_code: str = None, _=Depends(instructor_required)):
    """ Update only provided fields """
    action_db = await Action.get(id=action_id).prefetch_related("texts__language", "type")
    if not language_code:
        language_code = action_db.texts[0].language.code
    action_text, created = await ActionText.get_or_create(language_id=(await Language.get(code=language_code)).id,
                                                          action_id=action_db.id,
                                                          defaults={"name": "", "description": "", "hint": ""})
    if created and (action.name is None or action.description is None):
        raise HTTPException(status_code=400, detail="You must provide a name and a description when creating a new action translation")
    if "tag" in action.__fields_set__:
        action_db.tag = action.tag
    if "previous" in action.__fields_set__:
        action_db.previous_id = action.previous
    if "next" in action.__fields_set__:
        action_db.next_id = action.next
    if "type" in action.__fields_set__:
        action_db.type = await Type.get(name=action.type)
    if "choice" in action.__fields_set__:
        if action_db.type.name != "choice" and action.type is not "choice":
            raise HTTPException(status_code=400, detail="You can only update the choice of a choice action")
        action_db.left_target_action_id = action.choice.left.target if action.choice.left.target is not None else action_db.left_target_action_id
        action_db.right_target_action_id = action.choice.right.target if action.choice.right.target is not None else action_db.right_target_action_id
        action_text.left_choice = action.choice.left.name if action.choice.left.name is not None else action_text.left_choice
        action_text.right_choice = action.choice.right.name if action.choice.right.name is not None else action_text.right_choice
    if "targets" in action.__fields_set__:
        await action_db.targets.clear()
        targets_to_add = await Target.filter(id__in=action.targets)
        await action_db.targets.add(*targets_to_add)
    if "artifactID" in action.__fields_set__:
        action_db.artifact_id = action.artifactID
    if "position" in action.__fields_set__:
        action_db.x = action.position.x
        action_db.y = action.position.y
        action_db.z = action.position.z
    if "name" in action.__fields_set__:
        action_text.name = action.name
    if "description" in action.__fields_set__:
        action_text.description = action.description
    if "hint" in action.__fields_set__:
        action_text.hint = action.hint
    await action_db.save()
    await action_text.save()
    if not await verify_tag_unicity_in_activity(action_db.tag, action_db.previous_id, action_db.next_id, action_db.id):
        raise HTTPException(status_code=400, detail="Tag already used in this activity")  # transaction rollback
    # retourne l'objet modifié
    return await get_action(action_id, language_code)


@router.delete("/{action_id}")
@atomic()
async def delete_action(action_id: int, _=Depends(instructor_required)):
    """ Delete an action """
    # on regarde si la ressource est utilisée par une autre action
    action = await Action.get(id=action_id)
    if action.ressourcePath is not None:
        if await Action.filter(ressourcePath=action.ressourcePath).count() == 1:
            # si non on la supprime
            await aiofiles.os.remove(ACTION_DATA_DIRECTORY+action.ressourcePath)
    await Action.filter(id=action_id).delete()
    await ActionText.filter(action_id=action_id).delete()
    return OKResponse(ok="Action deleted")


async def verify_tag_unicity_in_activity(tag: str, left_id: int, right_id: int, center_id: int):
    """ Verify that the tag is unique in the activity with a recursive left and right search """
    async def verify_tag_unicity_left(action_id: int, tag: str):
        """ Recursive left search """
        if action_id is None or action_id == center_id:
            return True
        action = await Action.get(id=action_id)
        if action.tag == tag:
            return False
        if action.previous_id is not None:
            return await verify_tag_unicity_left(action.previous_id, tag)
        return True

    async def verify_tag_unicity_right(action_id: int, tag: str):
        """ Recursive right search """
        if action_id is None or action_id == center_id:
            return True
        action = await Action.get(id=action_id)
        if action.tag == tag:
            return False
        if action.next_id is not None:
            return await verify_tag_unicity_right(action.next_id, tag)
        return True
    left, right = await asyncio.gather(verify_tag_unicity_left(left_id, tag), verify_tag_unicity_right(right_id, tag))
    return left and right


async def delete_action_ressource_file(action: Action):
    """ Delete the ressource of an action"""
    if action.ressourcePath is not None:
        # on regarde si la ressource est utilisée par une autre action
        if await Action.filter(ressourcePath=action.ressourcePath).count() == 1:
            # si non on la supprime
            await aiofiles.os.remove(ACTION_DATA_DIRECTORY+action.ressourcePath)
        action.ressourcePath = None
        return True
    return False
