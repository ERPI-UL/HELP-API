from time import time
from fastapi import APIRouter, Depends, HTTPException
from pydantic import parse_obj_as
import tortoise
import utils
import Models
router = APIRouter()


@router.get("/users/{idUser}/sessions", response_model=Models.pagination)
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
        sessions = await Models.Session.filter(user__id=id).prefetch_related('user', 'scenario').offset((page - 1) * per_page).limit(per_page)
    lastPage = session_count // per_page
    if(page > lastPage):
        raise HTTPException(status_code=404, detail="Page non trouvée")
    return {
        'total': session_count,
        'per_page': per_page,
        'current_page': page,
        'last_page': lastPage,
        'data': parse_obj_as(list[Models.SessionOut], sessions)
    }


@router.get('/sessions/{idSession}')
async def readSession(id: int):
    session = await Models.Session.get(id=id).prefetch_related('user', 'scenario', 'playedSteps', 'playedSteps')
    return await sessionToJSON(session)


@router.post('/users/{idUser}/sessions')
async def createSession(id: int, session: Models.SessionIn, current_user: Models.User = Depends(utils.get_current_user_in_token)):
    if id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Vous n'avez pas les droits pour créer une session sur cette utilisateur")
    user = await Models.User.get(id=id)
    scenario = await Models.Scenario.get(id=session.scenarioid)
    session = await Models.Session.create(user=user, scenario=scenario, date=session.date, evaluation=session.evaluation)
    return {
        'id': session.id,
    }


@router.post('/sessions/{idSession}/playedSteps', response_model=Models.playedStepIn)
async def createPlayedStep(sessionid: int, playedStep: Models.playedStepPost, current_user: Models.User = Depends(utils.get_current_user_in_token)):
    session = await Models.Session.get(id=sessionid).prefetch_related('user')
    if session.user.id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Vous n'avez pas les droits pour créer une étape sur cette session")
    step = Models.playedStep(progressNumber=playedStep.progressNumber, missed=playedStep.missed,
                             skipped=playedStep.skipped, record=playedStep.record, step_id=playedStep.stepid, session_id=sessionid, time=playedStep.time)
    await step.save()
    return step


@router.delete('/sessions/playedSteps/{idPlayedStep}')
async def deletePlayedStep(id: int, current_user: Models.User = Depends(utils.get_current_user_in_token)):
    step = await Models.playedStep.filter(id=id).prefetch_related('session__user').first()
    if not step:
        raise HTTPException(status_code=404, detail="Step non trouvé")
    if step.session.user.id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Vous n'avez pas les droits pour supprimer cet objet")
    step = await step.delete()
    return {'message': 'deleted'}


@router.delete('/sessions/{idSession}/playedSteps')
async def deletePlayedSteps(sessionid: int, current_user: Models.User = Depends(utils.get_current_user_in_token)):
    session = await Models.Session.get(id=sessionid).prefetch_related('user')
    if session.user.id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Vous n'avez pas le droit de supprimer ces objets")
    steps = await Models.playedStep.filter(session__id=sessionid).all()
    for step in steps:
        await step.delete()
    return {'message': f"{steps.__len__()} étapes de progressions ont été supprimés"}


@router.delete('/sessions/{idSession}')
async def deleteSession(idSession: int, current_user: Models.User = Depends(utils.get_current_user)):
    session = await Models.Session.get(id=idSession).prefetch_related('user')
    if session.user.id != current_user.id and current_user.adminLevel < utils.Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=403, detail="Vous n'avez pas les droits pour supprimer cette session")
    await session.delete()
    return {
        'message': 'Session supprimée'
    }


async def sessionToJSON(session):
    return {
        'id': session.id,
        'scenario': {
            "id": session.scenario.id,
        },
        'date': session.date,
        'evaluation': session.evaluation,
        'playedSteps': [await playedStepToJSON(playedStep) for playedStep in session.playedSteps]
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


@router.get('/scenarios/backwardRate')
async def backwardRate(idScenario: int, idUser: int = None, current_user: Models.User = Depends(utils.get_current_user_in_token)):
    conn = tortoise.Tortoise.get_connection("default")
    if idUser:
        distinct = await conn.execute_query_dict('select  count(distinct step_id) from "playedSteps" inner join session s on s.id = "playedSteps".session_id where scenario_id=($1) and user_id=($2);', [idScenario, idUser])
        total = await conn.execute_query_dict('select count(*) from "playedSteps" inner join session s on s.id = "playedSteps".session_id where scenario_id=($1) and user_id=($2);', [idScenario, idUser])
    else:
        distinct = await conn.execute_query_dict('select  count(distinct step_id) from "playedSteps" inner join session s on s.id = "playedSteps".session_id where scenario_id=($1);', [idScenario])
        total = await conn.execute_query_dict('select count(*) from "playedSteps" inner join session s on s.id = "playedSteps".session_id where scenario_id=($1);', [idScenario])
    if total[0]['count'] == 0:
        raise HTTPException(
            status_code=404, detail="Aucune donnée trouvée")
    backwardRate = 1-(distinct[0]['count']/total[0]['count'])
    return {'scenario': idScenario, 'data': backwardRate}


@router.get('/scenarios/performRate')
# poucentage des utiliseurs qui réalise l'étape par scénario
async def performRate(idScenario: int, current_user: Models.User = Depends(utils.get_current_user_in_token)):
    # pour chaques étapes, un nombre entre 1-0 indicant le taux de personnes ayant fait cette etape du scenario
    conn = tortoise.Tortoise.get_connection("default")
    scenario = await Models.Scenario.get(id=idScenario).prefetch_related('steps')
    list = []
    numberOfTimeScenarioPlayed = await conn.execute_query_dict('select count(*) from session where scenario_id=($1);', [idScenario])
    for step in scenario.steps:
        playedSteps = await conn.execute_query_dict('select count(distinct step_id) from "playedSteps" inner join session s on s.id = "playedSteps".session_id where step_id = ($1) and scenario_id = ($2);', [step.id, idScenario])
        if playedSteps[0]['count'] == 0:
            list.append({'id': step.id, 'name': step.name, 'performRate': 0})
        else:
            list.append({'id': step.id, 'name': step.name,
                        'performRate': playedSteps[0]['count']/numberOfTimeScenarioPlayed[0]['count']})
    return {'scenario': scenario.id, 'data': list}


@router.get('/scenarios/performTime')
# nombre de fois ou moyenne où l'utilisateur réalise l'étape par scenario
async def performTime(idScenario: int, current_user: Models.User = Depends(utils.get_current_user_in_token)):
    conn = tortoise.Tortoise.get_connection("default")
    scenario = await Models.Scenario.get(id=idScenario).prefetch_related('steps')
    numberOfTimeScenarioPlayed = await conn.execute_query_dict('select count(*) from session where scenario_id=($1);', [idScenario])
    list = []
    for step in scenario.steps:
        playedSteps = await conn.execute_query_dict('select count(step_id) from "playedSteps" inner join session s on s.id = "playedSteps".session_id where step_id = ($1) and scenario_id = ($2);', [step.id, idScenario])
        list.append({'id': step.id, 'name': step.name,
                    'performTime': playedSteps[0]['count']/numberOfTimeScenarioPlayed[0]['count']})
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
        'step_id': playedStep.step_id,
        'time': playedStep.time,
    }
