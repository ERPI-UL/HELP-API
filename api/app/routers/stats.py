from fastapi import APIRouter, Depends, HTTPException
from pydantic import parse_obj_as
import utils
import Models
from tortoise.contrib.pydantic import pydantic_model_creator
from typing import List
from .scenarios import scenarioToJSON
router = APIRouter()


@router.get("/users/{id}/sessions", response_model=Models.pagination)
async def readSessions(id: int, page: int = 1, per_page: int = 10, id_scenario: int = None):
    session_count = await Models.Session.filter(user__id=id).count()
    if session_count < per_page:
        per_page = session_count
    # check for zero per_page
    if per_page == 0:
        per_page = 1
    if id_scenario:
        sessions = await Models.Session.filter(user__id=id, scenario__id=id_scenario).prefetch_related('user', 'scenario__steps', 'playedSteps', 'playedSteps__step').offset((page - 1) * per_page).limit(per_page)
    else:
        sessions = await Models.Session.filter(user__id=id).prefetch_related('user', 'scenario__steps', 'playedSteps', 'playedSteps__step').offset((page - 1) * per_page).limit(per_page)
    lastPage = session_count // per_page
    if(page > lastPage):
        raise HTTPException(status_code=404, detail="Page non trouvée")
    return {
        'total': session_count,
        'per_page': per_page,
        'current_page': page,
        'last_page': lastPage,
        'data': [await sessionToJSON(session) for session in sessions]
    }


@router.post('/users/{id}/sessions', response_model=Models.SessioninFront)
async def createSession(id: int, session: Models.SessionIn):
    user = await Models.User.get(id=id)
    scenario = await Models.Scenario.get(id=session.scenario)
    session = await Models.Session.create(user=user, scenario=scenario)
    return await sessionToJSON(session)


@router.post('/sessions/{sessionid}/playedSteps', response_model=Models.playedStepIn)
async def createPlayedStep(sessionid:int,playedStep: Models.playedStepPost):
    step = Models.playedStep(progressNumber=playedStep.progressNumber, missed=playedStep.missed, skipped=playedStep.skipped, record=playedStep.record, step_id=playedStep.stepid,session_id=sessionid)
    await step.save()
    return step
@router.delete('/sessions/{sessionid}/playedSteps')
async def deletePlayedSteps(sessionid:int,current_user:Models.User = Depends(utils.get_current_user_in_token)):
    session = await Models.Session.get(id=sessionid).prefetch_related('user')
    if session.user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Vous n'avez pas le droit de supprimer ces objets")
    steps = await Models.playedStep.filter(session__id=sessionid).all()
    for step in steps:
        await step.delete()
    return {'message': f"{steps.__len__()} étapes de progressions ont été supprimés"}
@router.delete('/sessions/playedSteps/{id}')
async def deletePlayedStep(id: int,current_user: Models.User = Depends(utils.get_current_user_in_token)):
    step = await Models.playedStep.filter(id=id).prefetch_related('session').first()
    if step.session.user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Vous n'avez pas les droits pour supprimer cet objet")
    step = step.delete()
    return {'message': 'deleted'}
async def sessionToJSON(session):
    return {
        'id': session.id,
        'scenario': await scenarioToJSON(session.scenario),
        'playedSteps': [await playedStepToJSON(playedStep) for playedStep in session.playedSteps],
    }


async def userToJSON(user):
    return {
        'id': user.id,
        'username': user.username,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'email': user.email,
    }


async def playedStepToJSON(playedStep):
    return {
        'id': playedStep.id,
        'progressNumber': playedStep.progressNumber,
        'missed': playedStep.missed,
        'skipped': playedStep.skipped,
        'recorded': playedStep.record,
        'step': playedStep.step,
    }
