from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.tortoise import paginate
from tortoise.exceptions import BaseORMException
from tortoise.transactions import atomic

from app.controllers.statement import find_object
from app.models.session import ActionStats, Session, SessionShort
from app.models.statement import (ContextOut, ResultInCreate, ScoreInCreate,
                                  Statement, StatementOut)
from app.types.stat import ActionStatsOut, ScenarioStats, SessionStat
from app.utils import (Permission, get_current_user_in_token,
                       insctructor_required)

router = APIRouter()


@router.get('/activities/{id_activity}', response_model=ScenarioStats)
async def get_activity_stats(id_activity: int, _=Depends(insctructor_required)):
    """
    Get average stats of all sessions of an activity
    """
    pass


@router.get("/users/{id_user}/sessions", response_model=Page[SessionShort])
async def get_user_sessions(id_user: int, user=Depends(get_current_user_in_token)):
    """ Get all sessions of a user """
    if user.id != id_user and user.adminLevel < Permission.INSTRUCTOR.value:
        raise HTTPException(status_code=403, detail="You don't have the permission to access this resource")
    return await paginate(Session.filter(user_id=id_user).prefetch_related("activity").order_by("-id").all())


@router.get("/sessions/{id_session}/stats")
async def get_session_stats(id_session: int, user=Depends(get_current_user_in_token)):
    """ Get all stats of a session """
    session = await Session.get(id=id_session).prefetch_related("actionStats", "actionStats__action")
    if user.id != session.user_id and user.adminLevel < Permission.INSTRUCTOR.value:
        raise HTTPException(status_code=403, detail="You don't have the permission to access this resource")
    if not session.computed:
        await compute_session(session)
    else:
        return SessionStat(
            id=session.id,
            activity_id=session.activity_id,
            user=session.user_id,
            start=session.start,
            end=session.end,
            duration=session.duration,
            abandoned=session.abandoned,
            actions=[
                ActionStatsOut(
                    id=action_stats.id,
                    action_id=action_stats.action_id,
                    tag=action_stats.action.tag,
                    start=action_stats.start,
                    end=action_stats.end,
                    duration=action_stats.duration,
                    completed=action_stats.completed,
                    skipped=action_stats.skipped,
                    help=action_stats.help,
                    interactions=action_stats.interactions,
                ) for action_stats in session.actionStats
            ],
            skipped=sum([1 for action_stats in session.actionStats if action_stats.skipped]),
            help=sum([action_stats.help for action_stats in session.actionStats]),
            interactions=sum([action_stats.interactions for action_stats in session.actionStats]),
        )


@router.get("/sessions/{id_session}/statements", response_model=list[StatementOut])
async def get_session_statements(id_session: int, user=Depends(get_current_user_in_token)):
    """ Get all statements of a session """
    statements = await Statement.filter(context_session_id=id_session).prefetch_related("object_activity", "object_target", "object_agent", "context_platform", "context_language").order_by("timestamp").all()
    if user.id != statements[0].actor_id and user.adminLevel < Permission.INSTRUCTOR.value:
        raise HTTPException(status_code=403, detail="You don't have the permission to access this resource")
    return [StatementOut(
        id=statement_db.id,
        actor=statement_db.actor_id,
        verb=statement_db.verb_id,
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
            )
        ),
        timestamp=statement_db.timestamp,
        stored=statement_db.stored
    ) for statement_db in statements]


async def compute_session(session: Session):
    pass


def find_object_type(statement: Statement):
    """ Find the type of the object of a statement """
    if statement.object_action_id is not None:
        return "action"
    if statement.object_activity_id is not None:
        return "activity"
    if statement.object_agent_id is not None:
        return "agent"
    if statement.object_target_id is not None:
        return "target"
    return None


@atomic()
async def parse_statement(statement: Statement):
    """
    Parse a statement to get the stats

    activity start is already handled in the router performance.py
    """
    try:
        match find_object_type(statement):
            case "action":
                session = await Session.get_or_none(id=statement.context_session_id)
                if session is None:
                    print("session not found")
                match statement.verb_id:
                    case "start":
                        played_action = await ActionStats.create(session=session, action_id=statement.object_action_id, start=statement.timestamp)
                    case "complete":
                        played_action = await ActionStats.get(session=session, action=statement.object_action_id, completed=False, end__isnull=True)
                        played_action.end = statement.timestamp
                        played_action.duration = (played_action.end - played_action.start).total_seconds()
                        played_action.completed = True
                        played_action.computed = True  # object is completed, no need to compute it again ( we should'nt interact with it anymore)
                        await played_action.save()
                    case "skip":
                        played_action = await ActionStats.get(session=session, action=statement.object_action_id)
                        played_action.skipped = True
                        played_action.end = statement.timestamp
                        played_action.duration = (played_action.end - played_action.start).total_seconds()
                        played_action.computed = True  # same thing as above
                        await played_action.save()
                    case "help":
                        played_action = await ActionStats.get(session=session, action=statement.object_action_id)
                        played_action.help += 1
                        await played_action.save()
            case "target":
                match statement.verb_id:
                    case "interact" | "press":
                        played_action = await ActionStats.get(action=statement.context_action_id, session__user_id=statement.actor_id)
                        played_action.interactions += 1
                        await played_action.save()
                    case "view":
                        pass
                    case "release":
                        pass
            case "activity":
                match statement.verb_id:
                    case "complete":
                        session = await Session.get(user=statement.actor_id, activity=statement.object_activity_id).order_by("-id").first()
                        session.end = statement.timestamp
                        session.duration = (session.end - session.start).total_seconds()
                        session.computed = True
                        await session.save()
            case "agent":
                pass
    except BaseORMException as exception:
        print(exception)
