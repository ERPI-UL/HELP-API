from time import process_time_ns
from fastapi import APIRouter, Depends, HTTPException
from pydantic import parse_obj_as
import tortoise
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
        sessions = await Models.Session.filter(user__id=id).prefetch_related('user', 'scenario__steps__targets', 'playedSteps', 'playedSteps__step').offset((page - 1) * per_page).limit(per_page)
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


@router.post('/users/{id}/sessions')
async def createSession(id: int, session: Models.SessionIn,current_user: Models.User = Depends(utils.get_current_user_in_token)):
    if id != current_user.id:
        raise HTTPException(status_code=403, detail="Vous n'avez pas les droits pour créer une session sur cette utilisateur")
    user = await Models.User.get(id=id)
    scenario = await Models.Scenario.get(id=session.scenarioid)
    session = await Models.Session.create(user=user, scenario=scenario)
    return {
        'id': session.id,
    }


@router.post('/sessions/{sessionid}/playedSteps', response_model=Models.playedStepIn)
async def createPlayedStep(sessionid: int, playedStep: Models.playedStepPost,current_user: Models.User = Depends(utils.get_current_user_in_token)):
    session = await Models.Session.get(id=sessionid).prefetch_related('user')
    if session.user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Vous n'avez pas les droits pour créer une étape sur cette session")
    step = Models.playedStep(progressNumber=playedStep.progressNumber, missed=playedStep.missed,
                             skipped=playedStep.skipped, record=playedStep.record, step_id=playedStep.stepid, session_id=sessionid)
    await step.save()
    return step


@router.delete('/sessions/{sessionid}/playedSteps')
async def deletePlayedSteps(sessionid: int, current_user: Models.User = Depends(utils.get_current_user_in_token)):
    session = await Models.Session.get(id=sessionid).prefetch_related('user')
    if session.user.id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Vous n'avez pas le droit de supprimer ces objets")
    steps = await Models.playedStep.filter(session__id=sessionid).all()
    for step in steps:
        await step.delete()
    return {'message': f"{steps.__len__()} étapes de progressions ont été supprimés"}

@router.delete('/sessions/playedSteps/{id}')
async def deletePlayedStep(id: int, current_user: Models.User = Depends(utils.get_current_user_in_token)):
    step = await Models.playedStep.filter(id=id).prefetch_related('session__user').first()
    if not step:
        raise HTTPException(status_code=404, detail="Step non trouvé")
    if step.session.user.id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Vous n'avez pas les droits pour supprimer cet objet")
    step = await step.delete()
    return {'message': 'deleted'}


async def sessionToJSON(session):
    return {
        'id': session.id,
        'scenario': await scenarioToJSON(session.scenario),
        'playedSteps': [await playedStepToJSON(playedStep) for playedStep in session.playedSteps],
    }


@router.get('/scenarios/averageTime')
async def averageTime(idScenario: int, current_user: Models.User = Depends(utils.get_current_user_in_token)):
    conn = tortoise.Tortoise.get_connection("default")
    scenario = await Models.Scenario.get(id=idScenario)
    res = await conn.execute_query_dict('select avg(time),step_id,s2.name from "playedSteps" inner join session s on "playedSteps".session_id = s.id inner join steps s2 on "playedSteps".step_id = s2.id where s.scenario_id = ($1) group by step_id,s2.name;', [idScenario])
    return {'scenario': scenario, 'data': res}


@router.get('/scenarios/skipRate')
async def skipRate(idScenario: int, current_user: Models.User = Depends(utils.get_current_user_in_token)):
    conn = tortoise.Tortoise.get_connection("default")
    scenario = await Models.Scenario.get(id=idScenario).prefetch_related('steps')
    print(scenario)
    list = []
    # FIXME: make this with full SQL query not 2 queries for each step
    for step in scenario.steps:
        skipped = await conn.execute_query_dict('select count(*) from "playedSteps" inner join session on session_id = session.id where skipped = true and step_id = ($1) and session.scenario_id = ($2);', [step.id, idScenario])
        total = await conn.execute_query_dict('select count(*) from "playedSteps" inner join session on session_id = session.id where step_id = ($1) and session.scenario_id = ($2);', [step.id, idScenario])
        if total[0]['count'] != 0:
            list.append({'id': step.id, 'name': step.name,
                        'skipRate': skipped[0]['count']/total[0]['count']})
        else:
            list.append({'id': step.id, 'name': step.name, 'skipRate': -1})
    return {'scenario': scenario.id, 'data': list}


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
