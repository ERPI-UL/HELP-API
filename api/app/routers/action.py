from fastapi.routing import APIRouter
from tortoise.transactions import atomic

from app.models.action import (Action, ActionIn, ActionInPatch, ActionOut,
                               ActionText)
from app.models.language import Language
from app.models.position import PositionPost
from app.models.type import Type
from app.types.response import IDResponse
from app.models.action import ChoiceOut, ChoiceMember

router = APIRouter()


@router.get("/{action_id}", response_model=ActionOut)
async def get_action(action_id: int, language_code: str = 'fr'):
    """ Get an action"""
    action = await Action.get(id=action_id).prefetch_related("texts", "type", "targets")
    action_text = await action.texts.filter(language__code=language_code).first()
    return ActionOut(
        id=action.id,
        name=action_text.name,
        description=action_text.description,
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


@router.post("/", response_model=IDResponse)
@atomic()
async def create_action(action: ActionIn):
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
        activity_id=action.activityID
    )
    await ActionText.create(
        name=action.name,
        description=action.description,
        language_id=(await Language.get(code=action.language)).id,
        action_id=action_db.id
    )
    return IDResponse(id=action_db.id)


@router.patch("/{action_id}", response_model=ActionOut)
@atomic()
async def update_action(action_id: int,  action: ActionInPatch, language_code: str = "fr"):
    """ Update only provided fields """
    action_db = await Action.get(id=action_id)
    action_text, created = await ActionText.get_or_create(language_id=(await Language.get(code=language_code)).id, action_id=action_db.id)
    if "tag" in action.__fields_set__:
        action_db.tag = action.tag
    if "previous" in action.__fields_set__:
        action_db.previous_id = action.previous
    if "next" in action.__fields_set__:
        action_db.next_id = action.next
    if "type" in action.__fields_set__:
        action_db.type = await Type.get(name=action.type)
        if action.type == "choice":
            action_db.left_target_action_id = action.choice.left.target
            action_db.right_target_action_id = action.choice.right.target
            action_text.left_choice = action.choice.left.name
            action_text.right_choice = action.choice.right.name
        else:
            action_db.left_target_action_id = None
            action_db.right_target_action_id = None
            action_text.left_choice = None
            action_text.right_choice = None
    if "targets" in action.__fields_set__:
        action_db.targets.clear()
        for target_id in action.targets:
            action_db.targets.add(await Action.get(id=target_id))
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
    await action_text.save()
    await action_db.save()

    # retourne l'objet modifié
    return await get_action(action_id, language_code)
