from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import parse_obj_as
from tortoise.contrib.pydantic import pydantic_model_creator
import Models
import utils
router = APIRouter()


@router.get("/", response_model=Models.pagination)
async def read_scenarios(idMachine: int = None, page: int = 1, per_page: int = 10):
    scenario_count = await Models.Scenario.all().count()
    if scenario_count < per_page:
        per_page = scenario_count
    # check for zero per_page
    if per_page == 0:
        per_page = 1
    lastPage = scenario_count // per_page
    if(page > lastPage):
        raise HTTPException(status_code=404, detail="Page not found")
    if idMachine:
        scenarios = await Models.Scenario.filter(machine=idMachine).offset((page - 1) * per_page).limit(per_page).prefetch_related('machine')
    else:
        scenarios = await Models.Scenario.all().offset((page - 1) * per_page).limit(per_page).prefetch_related('machine')
    return {
        'total': scenario_count,
        'per_page': per_page,
        'current_page': page,
        'last_page': lastPage,
        'data': [await shortScenarioToJSON(scenario) for scenario in scenarios]
    }


@router.delete('/machines/{machine_id}')
async def delete_machine(machine_id: int, user: Models.User = Depends(utils.InstructorRequired)):
    machine = await Models.Machine.get(id=machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine introuvable")
    await machine.delete()
    return {'ok': 'machine supprimée'}


@router.get('/machines', response_model=Models.pagination)
async def getMachines(page: int = 1, per_page: int = 10):
    machine_count = await Models.Machine.all().count()
    if machine_count < per_page:
        per_page = machine_count
    # check for zero per_page
    if per_page == 0:
        per_page = 1
    lastPage = machine_count // per_page
    if(page > lastPage):
        raise HTTPException(status_code=404, detail="Page non trouvée")
    machines = await Models.Machine.all().offset((page - 1) * per_page).limit(per_page).prefetch_related('scenarios')
    return {
        'total': machine_count,
        'per_page': per_page,
        'current_page': page,
        'last_page': lastPage,
        'data': parse_obj_as(list[Models.MachineOut], machines)
    }


@router.get('/machines/{machine_id}')
async def getMachine(machine_id: int):
    machine = await Models.Machine.get(id=machine_id).prefetch_related('targets')
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    return await machineWithTargetsToJSON(machine)


@router.post('/machines/{machine_id}/targets', response_model=list[Models.TargetOut])
async def createTarget(machine_id: int, targets: list, user: Models.User = Depends(utils.InstructorRequired)):
    machine = await Models.Machine.get(id=machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine introuvable")
    front = []
    for target in targets:
        target = Models.Target(name=target, machine=machine)
        await target.save()
        front.append(target)
    return parse_obj_as(list[Models.TargetOut], front)


@router.delete('/machines/targets/{target_id}')
async def deleteTarget(target_id: int, user: Models.User = Depends(utils.InstructorRequired)):
    target = await Models.Target.get(id=target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target introuvable")
    await target.delete()
    return {'ok': 'target supprimée'}


@router.put('/machines/targets/{target_id}')
async def updateTarget(target_id: int, target: Models.TargetPost, user: Models.User = Depends(utils.InstructorRequired)):
    targetInDB = await Models.Target.get(id=target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Cible introuvable")
    targetInDB.name = target.name
    await targetInDB.save()
    return {'ok': 'Cible mise à jour'}


@router.get('/{id}')
async def getScenario(id: int):
    scenario = await Models.Scenario.get(id=id).prefetch_related('machine').prefetch_related('steps').prefetch_related('steps__type').prefetch_related('steps__targets', 'steps__position', 'steps__choice')
    # scenario2 = await Models.Scenario.get(id=id).values('id', 'name', 'description', 'steps__id', 'steps__label', 'steps__name', 'steps__description')
    return await scenarioToJSON(scenario)


@router.post("/machines")
async def create_machine(machine: Models.Machinein, adminLevel: int = Depends(utils.getAdminLevel)):
    machine = utils.sanitizer(machine)
    if adminLevel < utils.Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return await Models.MachineOut.from_tortoise_orm(await Models.Machine.create(name=machine.name, description=machine.description))


@router.put('/machine/{id}')
async def update_machine(id: int, machine: Models.Machinein, adminLevel: int = Depends(utils.getAdminLevel)):
    machine = utils.sanitizer(machine)
    if adminLevel < utils.Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough rights")
    await Models.Machine.filter(id=id).update(name=machine.name, description=machine.description)
    return await Models.Machinein.from_tortoise_orm(await Models.Machine.get(id=id))


@router.post('/')
async def createScenario(scenario: Models.ScenarioPost, adminLevel: int = Depends(utils.getAdminLevel)):
    scenario = utils.sanitizer(scenario)
    if adminLevel < utils.Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough rights")
    scenario = await Models.Scenario.create(name=scenario.name, description=scenario.description, machine=await Models.Machine.get(id=scenario.machine.id))
    for step in scenario.steps:
        step.position = await Models.Position.create(x=step.position.x, y=step.position.y, z=step.position.z)
        step.type = await Models.Type.get(name=step.type.name).first()
        if step.type.name == 'choice':
            step.choice = await Models.Choice.create(labelleft=step.choice.option_left.label, labelright=step.choice.option_right.label, redirectleft=step.choice.option_left.redirect, redirectright=step.choice.option_right.redirect)
        step.targets = [await Models.Target.get(id=target) for target in step.targets]
        step.scenario = scenario
        await step.save()
    return {'id': scenario.id}


@router.put('/steps/{id}')
async def updateStep(id: int, step: pydantic_model_creator(Models.Step), adminLevel: int = Depends(utils.getAdminLevel)):
    step = utils.sanitizer(step)
    if adminLevel < utils.Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough rights")
    step.id = id
    await step.save()
    return await stepToJSON(step)


@router.get('/{idScenario}/step/{idStep}/target/{idTarget}')
async def getScenarioStepTargets(idScenario: int, idStep: int, idTarget: int):
    target = await Models.Target.filter(steps=idStep, id=idTarget).first()
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    return await targetToJSON(target)


async def scenarioToJSON(scenario):
    scenario.machine = await scenario.machine.get()
    return {
        'id': scenario.id,
        'name': scenario.name,
        'description': scenario.description,
        'machine': await machineToJSON(scenario.machine),
        'steps': [await stepToJSON(step) for step in scenario.steps]
    }


async def shortScenarioToJSON(scenario):
    return {
        'id': scenario.id,
        'name': scenario.name,
        'description': scenario.description,
        'machine': await machineToJSON(scenario.machine)
    }


async def stepToJSON(step):
    return {
        'id': step.id,
        'description': step.description,
        'label': step.label,
        'name': step.name,
        'position': await positionToJSON(step.position),
        'type': (await step.type.values('name'))[0]['name'],
        'choice': await choiceToJSON(step.choice),
        'targets': [await targetToJSON(target) for target in step.targets]
    }


async def targetToJSON(target):
    return {
        'id': target.id,
        'name': target.name,
    }


async def choiceToJSON(choice: Models.Choice):
    if choice:
        return {
            'id': choice.id,
            'option_left': {
                'label': choice.labelleft,
                'redirect': choice.redirectleft
            },
            'option_right': {
                'label': choice.labelright,
                'redirect': choice.redirectright
            },
        }


async def machineToJSON(machine):
    return {
        'id': machine.id,
        'name': machine.name,
        'description': machine.description
    }


async def positionToJSON(position: Models.Position):
    if not position:
        return None
    return {'x': position.x, 'y': position.y, 'z': position.z}


async def machineWithTargetsToJSON(machine):
    targets = []
    for target in machine.targets:
        targets.append({'id': target.id, 'name': target.name})
    return {
        'id': machine.id,
        'name': machine.name,
        'description': machine.description,
        'targets': targets
    }
