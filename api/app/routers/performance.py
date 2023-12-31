from datetime import datetime

from fastapi import BackgroundTasks, Depends, HTTPException
from fastapi.routing import APIRouter
from fastapi_pagination import Page
from fastapi_pagination.ext.tortoise import paginate

from app.models.language import Language
from app.models.platform import Platform
from app.models.session import Session
from app.models.statement import (ContextOut, ObjectOut, PlatformOut,
                                  ResultInCreate, ScoreInCreate, Statement,
                                  StatementInCreate, StatementOut, Verb)
from app.routers.stats import parse_statement
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
            ),
            extensions=statement_db.result_extensions
        ),
        timestamp=statement_db.timestamp,
        stored=statement_db.stored
    ) for statement_db in pagination.items]
    return pagination


def find_object(statement_db: Statement):
    """ find the object of a statement"""
    if statement_db.object_activity_id is not None:
        return ObjectOut(id=statement_db.object_activity_id, objectType="activity")
    elif statement_db.object_action_id is not None:
        return ObjectOut(id=statement_db.object_action_id, objectType="action")
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
            activity=statement_db.context_activity_id,
            session=statement_db.context_session_id
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
            ),
            extensions=statement_db.result_extensions
        ),
        timestamp=statement_db.timestamp,
        stored=statement_db.stored
    )


@router.post("/statements", response_model=StatementOut)
async def create_statement(statement: StatementInCreate, background_tasks: BackgroundTasks, user=Depends(get_current_user)):
    """ Send a statement to the LRS """
    platform_db, _ = await Platform.get_or_create(name=statement.context.platform)
    language_db = await Language.get_or_none(code=statement.context.language)
    verb_db = await Verb.get_or_none(id=statement.verb)
    if verb_db is None:
        raise HTTPException(status_code=404, detail="This verb does not exist in the LRS")
    if language_db is None:
        raise HTTPException(status_code=404, detail="This language does not exist in the LRS")
    if user.id != statement.actor:
        raise HTTPException(status_code=403, detail="You are not allowed to send a statement for another user")
    # FIXME: make an optional chaining function
    statement_db = await Statement.create(
        actor_id=user.id,
        verb=verb_db,
        object_activity_id=statement.object.id if statement.object.objectType == "activity" else None,
        object_agent_id=statement.object.id if statement.object.objectType == "agent" else None,
        object_target_id=statement.object.id if statement.object.objectType == "target" else None,
        object_action_id=statement.object.id if statement.object.objectType == "action" else None,
        context_platform=platform_db,
        context_language_id=language_db.id if language_db is not None else None,
        context_activity_id=statement.context.activity if statement.context is not None else None,
        context_session_id=statement.context.session if statement.context is not None else None,
        result_success=statement.result.success if statement.result is not None else None,
        result_completion=statement.result.completion if statement.result is not None else None,
        result_duration=statement.result.duration if statement.result is not None else None,
        result_response=statement.result.response if statement.result is not None else None,
        result_score_scaled=statement.result.score.scaled if statement.result is not None else None,
        result_score_raw=statement.result.score.raw if statement.result is not None else None,
        result_score_min=statement.result.score.min if statement.result is not None else None,
        result_score_max=statement.result.score.max if statement.result is not None else None,
        result_extensions=statement.result.extensions if statement.result is not None and statement.result.extensions is not None else dict(),
        timestamp=statement.timestamp if statement.timestamp is not None else datetime.now()
    )
    if statement_db.object_activity_id is not None and statement_db.verb_id == "start":
        # create a session
        session_db = await Session.create(
            user_id=statement_db.actor_id,
            activity_id=statement_db.object_activity_id,
            start=statement_db.timestamp)
        statement_db.context_session_id = session_db.id
        await statement_db.save()
    background_tasks.add_task(parse_statement, statement_db)
    return await get_statement(statement_db.id, user=user)
