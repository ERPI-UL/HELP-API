from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.tortoise import paginate
from tortoise.exceptions import BaseORMException
from tortoise.transactions import atomic

from app.models.session import ActionStats, Session, SessionShort
from app.models.statement import Statement
from app.types.stat import ScenarioStats, StepStat
from app.utils import Permission, get_current_user_in_token

router = APIRouter()


@router.get('/activities/{id_activity}', response_model=ScenarioStats)
async def get_scenario_stats(id_activity: int, _=Depends(get_current_user_in_token)):
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
    session = await Session.get(id=id_session).prefetch_related("actions")
    if user.id != session.user_id and user.adminLevel < Permission.INSTRUCTOR.value:
        raise HTTPException(status_code=403, detail="You don't have the permission to access this resource")
    if session.end is not None:
        duration = (session.end - session.start).total_seconds()
    else:
        last_action = await ActionStats.filter(session=session).order_by("-end").first()
        if last_action is not None and last_action.end is not None:
            duration = (last_action.end - session.start).total_seconds()
        else:
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
    """ Parse a statement to get the stats """
    try:
        match find_object_type(statement):
            case "action":
                session = await Session.get(user_id=statement.actor_id).order_by("-id").first()
                match statement.verb_id:
                    case "start":
                        played_action = await ActionStats.create(session=session, action_id=statement.object_action_id, start=statement.timestamp)
                    case "complete":
                        played_action = await ActionStats.get(session=session, action=statement.object_action_id, completed=False, end__isnull=True)
                        played_action.end = statement.timestamp
                        played_action.duration = (played_action.end - played_action.start).total_seconds()
                        played_action.completed = True
                        await played_action.save()
                    case "skip":
                        played_action = await ActionStats.get(session=session, action=statement.object_action_id)
                        played_action.skipped = True
                        played_action.end = statement.timestamp
                        played_action.duration = (played_action.end - played_action.start).total_seconds()
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
                    case "start":
                        await Session.create(user_id=statement.actor_id, activity_id=statement.object_activity_id, start=statement.timestamp)
                    case "complete":
                        session = await Session.get(user=statement.actor_id, activity=statement.object_activity_id).order_by("-id").first()
                        session.end = statement.timestamp
                        session.duration = (session.end - session.start).total_seconds()
                        await session.save()
            case "agent":
                pass
    except BaseORMException as exception:
        print(exception)
