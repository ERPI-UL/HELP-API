import tortoise
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import parse_obj_as
from tortoise import transactions
from tortoise.expressions import F, Q
from tortoise.functions import Count, Sum

from app.models.playedstep import PlayedStep, PlayedStepPost, playedStepIn
from app.types.stat import ScenarioStats
from app.models.session import Session, SessionIn, SessionOut
from app.types.stat import StepStat
from app.models.user import User
from app.models.scenario import Scenario
from app.types.pagination import Pagination
from app.utils import Permission, get_current_user, get_current_user_in_token

router = APIRouter()


@router.get("/users/{id_user}/sessions", response_model=Pagination)
async def get_user_sessions(id_user: int, page: int = 1, per_page: int = 10, id_scenario: int = None,
                            vrmode: bool = None, current_user: User = Depends(get_current_user_in_token)):
    """ Return a paginate list of all sessions of a user"""
    if id_user != current_user.id and current_user.adminLevel < Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    query = Session.filter(user__id=id_user)
    if id_scenario:
        query = query.filter(scenario__id=id_scenario)
    if vrmode is not None:
        query = query.filter(vrmode=vrmode)
    query.prefetch_related('user', 'scenario')
    session_count = await query.count()
    if session_count < per_page:
        per_page = session_count
    sessions = await query.offset((page - 1) * per_page).limit(per_page).order_by('-date')
    # check for zero per_page
    if per_page == 0:
        per_page = 1
    # calculate the number of pages
    last_page = session_count // per_page
    if session_count % per_page != 0:
        last_page += 1
    if page > last_page:
        raise HTTPException(status_code=404, detail="Page non trouvée")
    return {
        'total': session_count,
        'per_page': per_page,
        'current_page': page,
        'last_page': last_page,
        'data': parse_obj_as(list[SessionOut], sessions)
    }


@router.get('/sessions/{id_session}')
async def get_session(id_session: int, current_user: User = Depends(get_current_user_in_token)):
    """ Return a session by id """
    session = await Session.get(id=id_session).prefetch_related('user', 'scenario', 'playedSteps', 'playedSteps')
    if session.user.id != current_user.id and current_user.adminLevel < Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=403, detail="Cette session ne vous appartient pas")
    return await session_to_json(session)


@router.post('/users/{id_user}/sessions')
async def create_session(id_user: int, session: SessionIn, current_user: User = Depends(get_current_user_in_token)):
    """ Create a session for a user """
    if id_user != current_user.id:
        raise HTTPException(
            status_code=403, detail="Vous n'avez pas les droits pour créer une session sur cette utilisateur")
    user = await User.get(id=id_user)
    scenario = await Scenario.get(id=session.scenarioid)
    session = await Session.create(user=user, scenario=scenario, date=session.date, evaluation=session.evaluation, vrmode=session.vrmode)
    return {
        'id': session.id,
    }


@router.post('/sessions/{id_session}/playedSteps', response_model=playedStepIn)
async def create_played_step(id_session: int, played_step_in: PlayedStepPost, current_user: User = Depends(get_current_user_in_token)):
    """ Create a playedStep for a session """
    session = await Session.get(id=id_session).prefetch_related('user')
    if session.user.id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Vous n'avez pas les droits pour créer une étape sur cette session")
    step = PlayedStep(progressNumber=played_step_in.progressNumber, missed=played_step_in.missed,
                      skipped=played_step_in.skipped, record=played_step_in.record,
                      step_id=played_step_in.stepid, session_id=id_session, time=played_step_in.time)
    await step.save()
    return step


@router.delete('/sessions/playedSteps/{id_played_step}')
async def delete_played_step(id_played_step: int, current_user: User = Depends(get_current_user_in_token)):
    """ Delete a playedStep by id"""
    step = await PlayedStep.filter(id=id_played_step).prefetch_related('session__user').first()
    if not step:
        raise HTTPException(status_code=404, detail="Step non trouvé")
    if step.session.user.id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Vous n'avez pas les droits pour supprimer cet objet")
    step = await step.delete()
    return {'message': 'deleted'}


@router.delete('/sessions/{id_session}/playedSteps')
@transactions.atomic()
async def delete_played_steps(id_session: int, current_user: User = Depends(get_current_user_in_token)):
    """ Delete all playedSteps of a session """
    session = await Session.get(id=id_session).prefetch_related('user')
    if session.user.id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Vous n'avez pas le droit de supprimer ces objets")
    steps = await PlayedStep.filter(session__id=id_session).all()
    for step in steps:
        await step.delete()
    return {'message': f"{len(steps)} étapes de progressions ont été supprimés"}


@router.delete('/sessions/{id_session}')
async def delete_session(id_session: int, current_user: User = Depends(get_current_user)):
    """ Delete a session by id """
    session = await Session.get(id=id_session).prefetch_related('user')
    if session.user.id != current_user.id and current_user.adminLevel < Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=403, detail="Vous n'avez pas les droits pour supprimer cette session")
    await session.delete()
    return {
        'message': 'Session supprimée'
    }


async def session_to_json(session):
    """ Convert a session to JSON """
    return {
        'id': session.id,
        'scenario': {
            "id": session.scenario.id,
        },
        'vrmode': session.vrmode,
        'date': session.date,
        'evaluation': session.evaluation,
        'playedSteps': [await played_step_to_json(playedStep) for playedStep in session.playedSteps]
    }


@router.get('/scenarios/averageTime')
async def average_time(id_scenario: int, _: User = Depends(get_current_user_in_token)):
    """ Return the average time of a scenario"""
    conn = tortoise.Tortoise.get_connection("default")
    scenario = await Scenario.get(id=id_scenario)
    res = await conn.execute_query_dict("""select avg(time),step_id,s2.name from "playedSteps" inner join session s on "playedSteps".session_id
    = s.id inner join steps s2 on "playedSteps".step_id = s2.id where s.scenario_id = ($1) group by step_id,s2.name;""", [id_scenario])
    return {'scenario': scenario, 'data': res}


@router.get('/scenarios/skipRate')
async def skip_rate(id_scenario: int, vrmode: bool = None, _: User = Depends(get_current_user_in_token)):
    """ Return the skip rate for steps of a scenario """
    scenario = await Scenario.get(id=id_scenario).prefetch_related('steps')
    data_list = []
    # FIXME: make this with full SQL query not 2 queries for each step
    for step in scenario.steps:
        skipped_query = PlayedStep.filter(
            skipped=True, step_id=step.id, session__scenario_id=id_scenario)
        total_query = PlayedStep.filter(
            step_id=step.id, session__scenario_id=id_scenario)
        if vrmode is not None:
            skipped_query = skipped_query.filter(session__vrmode=vrmode)
            total_query = total_query.filter(session__vrmode=vrmode)
        skipped = await skipped_query.count()
        total = await total_query.count()
        if total != 0:
            data_list.append({'id': step.id, 'name': step.name,
                              'skipRate': skipped/total})
        else:
            data_list.append({'id': step.id, 'name': step.name, 'skipRate': -1})
    return {'scenario': scenario.id, 'data': data_list}


@router.get('/scenarios/backwardRate')
async def get_backward_rate(id_scenario: int, id_user: int = None, _: User = Depends(get_current_user_in_token)):
    """ Return the backward rate for each steps of a scenario """
    conn = tortoise.Tortoise.get_connection("default")
    if id_user:
        distinct = await conn.execute_query_dict("""select  count(distinct step_id) from "playedSteps" inner join session s
          on s.id = "playedSteps".session_id where scenario_id=($1) and user_id=($2);""", [id_scenario, id_user])
        total = await conn.execute_query_dict("""select count(*) from "playedSteps" inner join session s
        on s.id="playedSteps".session_id where scenario_id=($1) and user_id=($2); """, [id_scenario, id_user])
    else:
        distinct = await conn.execute_query_dict("""select  count(distinct step_id) from "playedSteps" inner join session s
        on s.id = "playedSteps".session_id where scenario_id=($1);""", [id_scenario])
        total = await conn.execute_query_dict("""select count(*) from "playedSteps" inner join session s
        on s.id="playedSteps".session_id where scenario_id=($1); """, [id_scenario])
    if total[0]['count'] == 0:
        raise HTTPException(
            status_code=404, detail="Aucune donnée trouvée")
    backward_rate = 1-(distinct[0]['count']/total[0]['count'])
    return {'scenario': id_scenario, 'data': backward_rate}


@router.get('/scenarios/performRate')
async def perform_rate(id_scenario: int, vrmode: bool = None, _: User = Depends(get_current_user_in_token)):
    """
    Pourcentage of users who perform a step in a scenario,
    for each step a number between 1-0 indicating the percentage
    of users who have done this step in the scenario
    """
    conn = tortoise.Tortoise.get_connection("default")
    scenario = Scenario.get(id=id_scenario).prefetch_related('steps')
    if vrmode is not None:
        scenario = scenario.filter(vrmode=vrmode)
    scenario = await scenario
    number_of_time_scernario_played = await Session.filter(scenario_id=id_scenario).count()
    data_list = []
    for step in scenario.steps:
        res = await conn.execute_query_dict("""select count(distinct step_id) from "playedSteps" inner join session s
        on s.id="playedSteps".session_id where step_id=($1) and scenario_id=($2); """, [step.id, id_scenario])
        if res[0]['count'] == 0:
            data_list.append({'id': step.id, 'name': step.name, 'performRate': 0})
        else:
            data_list.append({'id': step.id, 'name': step.name,
                              'performRate': res[0]['count']/number_of_time_scernario_played})
    return {'scenario': scenario.id, 'data': data_list}


@router.get('/scenarios/performTime')
async def perform_time(id_scenario: int, _=Depends(get_current_user_in_token)):
    """ number of times or average where the user performs the step by scenario"""
    conn = tortoise.Tortoise.get_connection("default")
    scenario = await Scenario.get(id=id_scenario).prefetch_related('steps')
    number_of_time_scenario_played = await conn.execute_query_dict('select count(*) from session where scenario_id=($1);', [id_scenario])
    data_list = []
    for step in scenario.steps:
        played_steps = await conn.execute_query_dict("""select count(step_id) from "playedSteps" inner join session s on
        s.id="playedSteps".session_id where step_id=($1) and scenario_id=($2); """, [step.id, id_scenario])
        data_list.append({'id': step.id, 'name': step.name,
                          'performTime': played_steps[0]['count']/number_of_time_scenario_played[0]['count']})
    return {'scenario': scenario.id, 'data': data_list}


@router.get("/scenarios/{id_scenario}", response_model=ScenarioStats)
async def get_scenario_stats(id_scenario: int, _=Depends(get_current_user_in_token)):
    """ Get scenario stats """
    scenario = await Scenario.get(id=id_scenario).prefetch_related('steps')
    total_played_time_for_scenario = await PlayedStep.annotate(
        value=Sum('time')
    ).values("value")
    total_success = await PlayedStep.filter(step__scenario_id=id_scenario, missed=False, skipped=False).count()
    total_played_time_for_scenario = total_played_time_for_scenario[0]["value"]
    number_of_vr_sessions = await Session.filter(scenario_id=id_scenario, vrmode=True).count()
    number_of_ar_sessions = await Session.filter(scenario_id=id_scenario, vrmode=False).count()
    number_of_sessions = number_of_ar_sessions + number_of_vr_sessions
    list_of_success_by_step = await PlayedStep.filter(session__scenario_id=id_scenario).annotate(
        step_id=F('step_id'),
        count=Count('step_id', _filter=Q(missed=False, skipped=False))
    ).group_by('step_id').values_list("step_id", "count")
    list_of_time_by_step = await PlayedStep.filter(session__scenario_id=id_scenario).annotate(
        step_id=F('step_id'),
        count=Sum('time')
    ).group_by('step_id').values_list("step_id", "count")
    average_time_by_step = list()
    list_of_step = await PlayedStep.filter(session__scenario_id=id_scenario).annotate(
        step_id=F('step_id'),
        count=Count('step_id')
    ).group_by('step_id').values_list("step_id", "count")
    average_success_rate_by_step = list()
    step_name = {step.id: step.name for step in scenario.steps}
    for i in list_of_success_by_step:
        average_success_rate_by_step.append(StepStat(
            id=i[0],
            value=i[1]/list_of_step[list_of_success_by_step.index(i)][1],
            name=step_name[i[0]]
        ))
    for i in list_of_time_by_step:
        average_time_by_step.append(StepStat(
            id=i[0],
            value=i[1]/list_of_step[list_of_time_by_step.index(i)][1],
            name=step_name[i[0]]
        ))
    return ScenarioStats(
        id=scenario.id,
        averageTime=(total_played_time_for_scenario / number_of_sessions),
        averageSuccessRate=total_success/number_of_sessions,
        numberOfVRSessions=number_of_vr_sessions,
        numberOfARSessions=number_of_ar_sessions,
        averageSuccessRateByStep=average_success_rate_by_step,
        averageTimeByStep=average_time_by_step,
    )


async def user_to_json(user):
    """Convert user to JSON"""
    return {
        'id': user.id,
        'username': user.username,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'email': user.email,
    }


async def played_step_to_json(played_step):
    """Convert playedStep to JSON"""
    return {
        'id': played_step.id,
        'progressNumber': played_step.progressNumber,
        'missed': played_step.missed,
        'skipped': played_step.skipped,
        'recorded': played_step.record,
        'step_id': played_step.step_id,
        'time': played_step.time,
    }
