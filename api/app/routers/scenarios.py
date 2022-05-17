from email import utils
from fastapi import APIRouter, Depends, HTTPException, status
from tortoise.contrib.pydantic import pydantic_model_creator
import Models
import utils
router = APIRouter()


@router.get("/", response_model=Models.pagination)
async def read_scenarios(page: int = 1, per_page: int = 10):
    scenario_count = await Models.Scenario.all().count()
    if scenario_count < per_page:
        per_page = scenario_count
    # check for zero per_page
    if per_page == 0:
        per_page = 1
    lastPage = scenario_count // per_page
    if(page > lastPage):
        raise HTTPException(status_code=404, detail="Page not found")
    scenarios = await Models.Scenario.all().offset((page - 1) * per_page).limit(per_page).prefetch_related('machine')
    return {
        'total': scenario_count,
        'per_page': per_page,
        'current_page': page,
        'last_page': lastPage,
        'data': [await shortScenarioToJSON(scenario) for scenario in scenarios]
    }


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
    for step in scenario.steps:
        step.position = await Models.Position.create(x=step.position.x, y=step.position.y, z=step.position.z)
        step.type = await Models.Type.get(name=step.type.name).first()
        if step.type.name == 'choice':
            step.choice = await Models.Choice.create(labelleft=step.choice.option_left.label, labelright=step.choice.option_right.label, redirectleft=step.choice.option_left.redirect, redirectright=step.choice.option_right.redirect)
        step.targets = [await Models.Target.get(id=target) for target in step.targets]
    scenario = await Models.Scenario.create(name=scenario.name, description=scenario.description, machine=await Models.Machine.get(id=scenario.machine.id))    
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
    return target.name


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
