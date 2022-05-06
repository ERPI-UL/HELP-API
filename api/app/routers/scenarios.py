from ctypes import util
from email import utils
from fastapi import APIRouter, Depends, HTTPException, status
from tortoise.contrib.pydantic import pydantic_model_creator
import Models
import utils
router = APIRouter()


@router.get("/")
async def read_scenarios():
    return [await scenarioToJSON(scenario) for scenario in await Models.Scenario.all().prefetch_related('steps').prefetch_related('steps__type').prefetch_related('steps__targets')]


@router.get('/{id}')
async def getScenario(id: int):
    scenario = await Models.Scenario.get(id=id).prefetch_related('steps').prefetch_related('steps__type').prefetch_related('steps__targets')
    # scenario2 = await Models.Scenario.get(id=id).values('id', 'name', 'description', 'steps__id', 'steps__label', 'steps__name', 'steps__description')
    return await scenarioToJSON(scenario)


@router.post("/machines")
async def create_machine(machine: Models.Machinein, adminLevel: int = Depends(utils.getAdminLevel)):
    if adminLevel < utils.Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return await Models.Machinein.from_tortoise_orm(await Models.Machine.create(name=machine.name, description=machine.description))


@router.put('/machine/{id}')
async def update_machine(id: int, machine: Models.Machinein, adminLevel: int = Depends(utils.getAdminLevel)):
    if adminLevel < utils.Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough rights")
    await Models.Machine.filter(id=id).update(name=machine.name, description=machine.description)
    return await Models.Machinein.from_tortoise_orm(await Models.Machine.get(id=id))


@router.get('/{idScenario}/step/{idStep}')
async def getScenarioSteps(idScenario: int, idStep: int):
    step = await Models.Step.filter(scenario_id=idScenario, id=idStep).prefetch_related('type').prefetch_related('targets').first()
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")
    return await stepToJSON(step)


@router.post('/')
async def createScenario(scenario: Models.ScenarioPost, adminLevel: int = Depends(utils.getAdminLevel)):
    if adminLevel < utils.Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough rights")
    scenario = await Models.Scenario.create(name=scenario.name, description=scenario.description)
    return {'id': scenario.id}


@router.put('/steps/{id}')
async def updateStep(id: int, step: pydantic_model_creator(Models.Step), adminLevel: int = Depends(utils.getAdminLevel)):
    if adminLevel < utils.Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough rights")
    step.id = id
    await step.save()
    return await stepToJSON(step)


@router.get('/{idScenario}/step/{idStep}/target/{idTarget}')
async def getScenarioStepTargets(idScenario: int, idStep: int, idTarget: int):
    target = await Models.Target.filter(step_id=idStep, id=idTarget).prefetch_related('type').prefetch_related('targets').first()
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    return await targetToJSON(target)


async def scenarioToJSON(scenario):
    return {
        'id': scenario.id,
        'name': scenario.name,
        'machine': 'ML-w960',
        'description': scenario.description,
        'steps': [await stepToJSON(step) for step in scenario.steps]
    }


async def stepToJSON(step):
    return {
        'id': step.id,
        'description': step.description,
        'label': step.label,
        'name': step.name,
        'type': (await step.type.values('name'))[0]['name'],
        'choice': "choix bidon",
        'targets': [await targetToJSON(target) for target in step.targets]
    }


async def targetToJSON(target):
    return {
        'id': target.id,
        'label': target.label,
        'name': target.name
    }


async def choiceToJSON(choice):
    return {
        'id': choice.id,
        'label': choice.label,
        'name': choice.name,
        'target': choice.target.name
    }


async def machineToJSON(machine):
    return {
        'id': machine.id,
        'name': machine.name,
        'description': machine.description
    }
