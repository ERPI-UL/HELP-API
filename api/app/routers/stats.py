from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import parse_obj_as
import tortoise
import utils
import Models
from tortoise.functions import Count
router = APIRouter()


@router.get("/users/{idUser}/sessions", response_model=Models.pagination)
async def readSessions(idUser: int, page: int = 1, per_page: int = 10, id_scenario: int = None, vrmode: bool = None, current_user: Models.User = Depends(utils.get_current_user_in_token)):
    if idUser != current_user.id and current_user.adminLevel < utils.Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    query = Models.Session.filter(user__id=idUser)
    if id_scenario:
        query = query.filter(scenario__id=id_scenario)
    if vrmode is not None:
        query = query.filter(vrmode=vrmode)
    query.prefetch_related('user', 'scenario')
    session_count = await query.count()
    if session_count < per_page:
        per_page = session_count
    sessions = await query.offset((page - 1) * per_page).limit(per_page)
    # check for zero per_page
    if per_page == 0:
        per_page = 1
    # calculate the number of pages
    lastPage = session_count // per_page
    if session_count % per_page != 0:
        lastPage += 1
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
async def readSession(idSession: int, current_user: Models.User = Depends(utils.get_current_user_in_token)):
    session = await Models.Session.get(id=idSession).prefetch_related('user', 'scenario', 'playedSteps', 'playedSteps')
    if session.user.id != current_user.id and current_user.adminLevel < utils.Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=403, detail="Cette session ne vous appartient pas")
    return await sessionToJSON(session)


@router.post('/users/{idUser}/sessions')
async def createSession(idUser: int, session: Models.SessionIn, current_user: Models.User = Depends(utils.get_current_user_in_token)):
    if idUser != current_user.id:
        raise HTTPException(
            status_code=403, detail="Vous n'avez pas les droits pour créer une session sur cette utilisateur")
    user = await Models.User.get(id=idUser)
    scenario = await Models.Scenario.get(id=session.scenarioid)
    session = await Models.Session.create(user=user, scenario=scenario, date=session.date, evaluation=session.evaluation)
    return {
        'id': session.id,
    }


@router.post('/sessions/{idSession}/playedSteps', response_model=Models.playedStepIn)
async def createPlayedStep(idSession: int, playedStep: Models.playedStepPost, current_user: Models.User = Depends(utils.get_current_user_in_token)):
    session = await Models.Session.get(id=idSession).prefetch_related('user')
    if session.user.id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Vous n'avez pas les droits pour créer une étape sur cette session")
    step = Models.playedStep(progressNumber=playedStep.progressNumber, missed=playedStep.missed,
                             skipped=playedStep.skipped, record=playedStep.record, step_id=playedStep.stepid, session_id=idSession, time=playedStep.time)
    await step.save()
    return step


@router.delete('/sessions/playedSteps/{idPlayedStep}')
async def deletePlayedStep(idPlayedStep: int, current_user: Models.User = Depends(utils.get_current_user_in_token)):
    step = await Models.playedStep.filter(id=idPlayedStep).prefetch_related('session__user').first()
    if not step:
        raise HTTPException(status_code=404, detail="Step non trouvé")
    if step.session.user.id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Vous n'avez pas les droits pour supprimer cet objet")
    step = await step.delete()
    return {'message': 'deleted'}


@router.delete('/sessions/{idSession}/playedSteps')
async def deletePlayedSteps(idSession: int, current_user: Models.User = Depends(utils.get_current_user_in_token)):
    session = await Models.Session.get(id=idSession).prefetch_related('user')
    if session.user.id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Vous n'avez pas le droit de supprimer ces objets")
    steps = await Models.playedStep.filter(session__id=idSession).all()
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
        'vrmode': session.vrmode,
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
async def skipRate(idScenario: int,vrmode:bool=None, current_user: Models.User = Depends(utils.get_current_user_in_token)):
    scenario = await Models.Scenario.get(id=idScenario).prefetch_related('steps')
    list = []
    # FIXME: make this with full SQL query not 2 queries for each step
    for step in scenario.steps:
        skippedQuery = Models.playedStep.filter(skipped=True, step_id=step.id, session__scenario_id=idScenario)
        totalQuery = Models.playedStep.filter(step_id=step.id, session__scenario_id=idScenario)
        if vrmode is not None:
            skippedQuery = skippedQuery.filter(session__vrmode=vrmode)
            totalQuery = totalQuery.filter(session__vrmode=vrmode)
        skipped = await skippedQuery.count()
        total = await totalQuery.count()
        if total != 0:
            list.append({'id': step.id, 'name': step.name,
                        'skipRate': skipped/total})
        else:
            list.append({'id': step.id, 'name': step.name, 'skipRate': -1})
    return {'scenario': scenario.id, 'data': list}


@router.get('/scenarios/backwardRate')
async def backwardRate(idScenario: int, idUser: int = None,vrmode:bool=None, current_user: Models.User = Depends(utils.get_current_user_in_token)):
    distinctQuery = Models.playedStep.filter(session__scenario_id=idScenario)
    totalQuery = Models.playedStep.filter(session__scenario_id=idScenario)
    if idUser is not None:
        distinctQuery = distinctQuery.filter(session__user_id=idUser)
        totalQuery = totalQuery.filter(session__user_id=idUser)
    if vrmode is not None:
        distinctQuery = distinctQuery.filter(session__vrmode=vrmode)
        totalQuery = totalQuery.filter(session__vrmode=vrmode)
    distinct = await distinctQuery.distinct().count()
    total = await totalQuery.count()
    if total == 0:
        raise HTTPException(
            status_code=404, detail="Aucune donnée trouvée")
    backwardRate = 1-(distinct/total)
    return {'scenario': idScenario, 'data': backwardRate}


@router.get('/scenarios/performRate')
# poucentage des utiliseurs qui réalise l'étape par scénario
async def performRate(idScenario: int,vrmode:bool=None, current_user: Models.User = Depends(utils.get_current_user_in_token)):
    # pour chaques étapes, un nombre entre 1-0 indicant le taux de personnes ayant fait cette etape du scenario
    conn = tortoise.Tortoise.get_connection("default")
    scenario = Models.Scenario.get(id=idScenario).prefetch_related('steps')
    if vrmode is not None:
        scenario = scenario.filter(vrmode=vrmode)
    scenario = await scenario
    numberOfTimeScenarioPlayed = await Models.Session.filter(scenario_id=idScenario).count()
    list = []
    for step in scenario.steps:
        playedSteps = await conn.execute_query_dict('select count(distinct step_id) from "playedSteps" inner join session s on s.id = "playedSteps".session_id where step_id = ($1) and scenario_id = ($2);', [step.id, idScenario])
        if playedSteps[0]['count'] == 0:
            list.append({'id': step.id, 'name': step.name, 'performRate': 0})
        else:
            list.append({'id': step.id, 'name': step.name,
                        'performRate': playedSteps[0]['count']/numberOfTimeScenarioPlayed})
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
