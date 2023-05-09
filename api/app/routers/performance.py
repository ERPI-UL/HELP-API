from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from fastapi_pagination import Page
from fastapi_pagination.ext.tortoise import paginate

from app.models.language import Language
from app.models.platform import Platform
from app.models.statement import (ContextOut, ObjectOut, PlatformOut,
                                  ResultInCreate, ScoreInCreate, Statement,
                                  StatementInCreate, StatementOut, Verb)
from app.utils import Permission, get_current_user

router = APIRouter()


@router.get("/platforms", response_model=list[PlatformOut])
async def get_platforms():
    """ get all platforms """
    return await Platform.all()


@router.get("/statements", response_model=Page)
async def get_statements(actor_id: int = None, verb: str = None, object_id: int = None, platform_name: str = None, user=Depends(get_current_user)):
    """ get all statements with pagination """
    query = Statement.all().prefetch_related("object_activity", "object_target", "object_agent", "context_platform", "context_language").order_by("-id")
    if user.adminLevel < Permission.ADMIN.value:
        query = query.filter(actor_id=user.id)
    if actor_id is not None and user.adminLevel >= Permission.ADMIN.value:
        query = query.filter(actor_id=actor_id)
    if verb is not None:
        query = query.filter(verb_id=verb)
    if object_id is not None:
        query = query.filter(object_activity_id=object_id)
    if platform_name is not None:
        query = query.filter(context_platform__name=platform_name)
    pagination = await paginate(query)
    pagination.items = [StatementOut(
        id=statement_db.id,
        actor=statement_db.actor_id,
        verb=statement_db.verb_id,
        object=find_object(statement_db),
        context=ContextOut(
            platform=statement_db.context_platform.name,
            language=statement_db.context_language.code,
            activity=statement_db.context_activity_id
        ),
        result=ResultInCreate(
            success=statement_db.result_success,
            completion=statement_db.result_completion,
            duration=statement_db.result_duration,
            response=statement_db.result_response,
            score=ScoreInCreate(
                scaled=statement_db.result_score_scaled,
                raw=statement_db.result_score_raw,
                min=statement_db.result_score_min,
                max=statement_db.result_score_max
            )
        ),
        timestamp=statement_db.timestamp,
        stored=statement_db.stored
    ) for statement_db in pagination.items]
    return pagination


def find_object(statement_db: Statement):
    """ find the object of a statement"""
    if statement_db.object_activity_id is not None:
        return ObjectOut(id=statement_db.object_activity_id, objectType="activity")
    elif statement_db.object_agent_id is not None:
        return ObjectOut(id=statement_db.object_agent_id, objectType="agent")
    elif statement_db.object_target_id is not None:
        return ObjectOut(id=statement_db.object_target_id, objectType="target")
    else:
        return None


@router.get("/statements/{statement_id}", response_model=StatementOut)
async def get_statement(statement_id: int, user=Depends(get_current_user)):
    """ get a statement """
    statement_db = await Statement.get(id=statement_id).prefetch_related("verb", "actor", "object_activity", "object_target", "object_agent", "context_platform", "context_language")
    if user.adminLevel < Permission.ADMIN.value and statement_db.actor_id != user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to access this statement")
    return StatementOut(
        id=statement_db.id,
        actor=statement_db.actor_id,
        verb=statement_db.verb.id,
        object=find_object(statement_db),
        context=ContextOut(
            platform=statement_db.context_platform.name,
            language=statement_db.context_language.code if statement_db.context_language is not None else None,
            activity=statement_db.context_activity_id
        ),
        result=ResultInCreate(
            success=statement_db.result_success,
            completion=statement_db.result_completion,
            duration=statement_db.result_duration,
            response=statement_db.result_response,
            score=ScoreInCreate(
                scaled=statement_db.result_score_scaled,
                raw=statement_db.result_score_raw,
                min=statement_db.result_score_min,
                max=statement_db.result_score_max
            )
        ),
        timestamp=statement_db.timestamp,
        stored=statement_db.stored
    )


@router.post("/statements", response_model=StatementOut)
async def create_statement(statement: StatementInCreate, user=Depends(get_current_user)):
    """ Send a statement to the LRS """
    platform_db, _ = await Platform.get_or_create(name=statement.context.platform)
    language_db = await Language.get_or_none(code=statement.context.language)
    verb_db = await Verb.get_or_none(id=statement.verb)
    if verb_db is None:
        raise HTTPException(status_code=404, detail="This verb does not exist in the LRS")
    if user.id != statement.actor:
        raise HTTPException(status_code=403, detail="You are not allowed to send a statement for another user")
    statement_db = await Statement.create(
        actor_id=statement.actor,
        verb=verb_db,
        object_activity_id=statement.object.id if statement.object.objectType == "activity" else None,
        object_agent_id=statement.object.id if statement.object.objectType == "agent" else None,
        object_target_id=statement.object.id if statement.object.objectType == "target" else None,
        context_platform=platform_db,
        context_language_id=language_db.id if language_db is not None else None,
        context_activity_id=statement.context.activity,
        result_success=statement.result.success,
        result_completion=statement.result.completion,
        result_duration=statement.result.duration,
        result_response=statement.result.response,
        result_score_scaled=statement.result.score.scaled,
        result_score_raw=statement.result.score.raw,
        result_score_min=statement.result.score.min,
        result_score_max=statement.result.score.max,
        result_extensions=statement.extensions,
        timestamp=statement.timestamp
    )
    return await get_statement(statement_db.id, user=user)
