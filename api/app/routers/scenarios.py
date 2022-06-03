from fastapi import APIRouter, Body, Depends, HTTPException, UploadFile, status, File
from fastapi.responses import FileResponse
from pydantic import parse_obj_as
from tortoise.contrib.pydantic import pydantic_model_creator
import Models
import utils
import aiofiles
import aiofiles.os
router = APIRouter()


@router.get("/", response_model=Models.pagination)
async def read_scenarios(idMachine: int = None, page: int = 1, per_page: int = 10):
    # check for zero per_page
    if per_page == 0:
        per_page = 1
    if idMachine:
        scenario_count = await Models.Scenario.filter(machine=idMachine).count()
        if scenario_count < per_page:
            per_page = scenario_count
        scenarios = await Models.Scenario.filter(machine=idMachine).offset((page - 1) * per_page).limit(per_page).prefetch_related('machine')
    else:
        scenario_count = await Models.Scenario.all().count()
        if scenario_count < per_page:
            per_page = scenario_count
        scenarios = await Models.Scenario.all().offset((page - 1) * per_page).limit(per_page).prefetch_related('machine')
    # calculate the number of pages
    lastPage = scenario_count // per_page
    if scenario_count % per_page != 0:
        lastPage += 1
    if(page > lastPage):
        raise HTTPException(status_code=404, detail="Page not found")
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
    # calculate the number of pages
    lastPage = machine_count // per_page
    if machine_count % per_page != 0:
        lastPage += 1
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


@router.get('/machines/{machine_id}/model', response_class=FileResponse)
async def getMachineModel(machine_id: int):
    machine = await Models.Machine.get(id=machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine introuvable")
    try:
        # test if file exists
        await aiofiles.os.stat(machine.path)
        return FileResponse(
            machine.path, media_type='application/octet-stream', filename=machine.name+'.fbx')  # FastApi will automatically find the file and return it
    except Exception:
        raise HTTPException(status_code=404, detail="Model introuvable")


@router.post('/machines/{machine_id}/model')
async def postMachineModel(machine_id: int, model: UploadFile = File(...), user: Models.User = Depends(utils.InstructorRequired)):
    machine = await Models.Machine.get(id=machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine introuvable")
    machine.path = utils.MODELS_DIRECTORY+str(machine.id)+"/machine.fbx"
    try:
        contents = await model.read()
        # create the directory if it doesn't exist
        await aiofiles.os.makedirs(utils.MODELS_DIRECTORY+str(machine.id), exist_ok=True)
        async with aiofiles.open(machine.path, 'wb') as f:
            await f.write(contents)
        await machine.save()
    except Exception:
        raise HTTPException(
            status_code=500, detail="Erreur lors de l'enregistrement du fichier")
    finally:
        await model.close()

    return {"ok": f" fichier envoyé : {model.filename}"}


@router.post('/machines/{machine_id}/targets', response_model=Models.TargetOut)
async def createTarget(machine_id: int, name: str = Body(..., embed=True), user: Models.User = Depends(utils.InstructorRequired)):
    machine = await Models.Machine.get(id=machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine introuvable")
    target = Models.Target(name=name, machine=machine)
    await target.save()
    return parse_obj_as(Models.TargetOut, target)


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


@router.get('/{idScenario}')
async def getScenario(idScenario: int):
    scenario = await Models.Scenario.get(id=idScenario).prefetch_related('machine').prefetch_related('steps').prefetch_related('steps__type').prefetch_related('steps__targets', 'steps__position', 'steps__choice')
    # scenario2 = await Models.Scenario.get(id=id).values('id', 'name', 'description', 'steps__id', 'steps__label', 'steps__name', 'steps__description')
    return await scenarioToJSON(scenario)


@router.delete('/{idScenario}')
async def delete_scenario(idScenario: int, user: Models.User = Depends(utils.InstructorRequired)):
    scenario = await Models.Scenario.get(id=idScenario)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario introuvable")
    await scenario.delete()
    return {'ok': 'scenario et objets référencés supprimés'}


@router.post("/machines")
async def create_machine(machine: Models.Machinein, adminLevel: int = Depends(utils.getAdminLevel)):
    if adminLevel < utils.Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return await Models.MachineOut.from_tortoise_orm(await Models.Machine.create(name=machine.name, description=machine.description))


@router.put('/machines/{idMachine}')
async def update_machine(idMachine: int, machine: Models.Machinein, adminLevel: int = Depends(utils.getAdminLevel)):
    if adminLevel < utils.Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough rights")
    await Models.Machine.filter(id=idMachine).update(name=machine.name, description=machine.description)
    return await Models.Machinein.from_tortoise_orm(await Models.Machine.get(id=idMachine))


@router.post('/')
async def createScenario(scenario: Models.ScenarioPost, adminLevel: int = Depends(utils.getAdminLevel)):
    if adminLevel < utils.Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough rights")
    scenarioDB = await Models.Scenario.create(name=scenario.name, description=scenario.description, machine=await Models.Machine.get(id=scenario.machine.id))
    for step in scenario.steps:
        position = await Models.Position.create(x=step.position.x, y=step.position.y, z=step.position.z)
        type = await Models.Type.get(name=step.type.name).first()
        stepDB = Models.Step(scenario=scenarioDB, type=type, label=step.label, position=position,
                             name=step.name, description=step.description, ordernumber=step.ordernumber)
        if step.type.name == 'choice':
            stepDB.choice = await Models.Choice.create(labelleft=step.choice.option_left.label, labelright=step.choice.option_right.label, redirectleft=step.choice.option_left.redirect, redirectright=step.choice.option_right.redirect)
        await stepDB.save()
        for target in step.targets:
            await stepDB.targets.add(await Models.Target.get(id=target))
    return {'id': scenarioDB.id}


@router.post('/{idScenario}/steps')
async def createStep(idScenario: int, step: Models.StepPost, adminLevel: int = Depends(utils.getAdminLevel)):
    if adminLevel < utils.Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough rights")
    scenario = await Models.Scenario.get(id=idScenario)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario introuvable")
    position = await Models.Position.create(x=step.position.x, y=step.position.y, z=step.position.z)
    type = await Models.Type.get(name=step.type.name).first()
    stepDB = Models.Step(scenario=scenario, type=type, label=step.label, position=position,
                         name=step.name, description=step.description, ordernumber=step.ordernumber)
    if step.type.name == 'choice':
        stepDB.choice = await Models.Choice.create(labelleft=step.choice.option_left.label, labelright=step.choice.option_right.label, redirectleft=step.choice.option_left.redirect, redirectright=step.choice.option_right.redirect)
    await stepDB.save()
    for target in step.targets:
        await stepDB.targets.add(await Models.Target.get(id=target))
    return {'id': stepDB.id}


@router.put('/steps/{idStep}')
async def updateStep(idStep: int, step: Models.StepPost, adminLevel: int = Depends(utils.getAdminLevel)):
    if adminLevel < utils.Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough rights")
    stepDB = await Models.Step.get(id=idStep).prefetch_related('targets', 'position', 'choice')
    if not stepDB:
        raise HTTPException(status_code=404, detail="Step introuvable")
    stepDB.label = step.label
    stepDB.name = step.name
    stepDB.description = step.description
    stepDB.ordernumber = step.ordernumber
    stepDB.type = await Models.Type.get(name=step.type.name).first()
    if step.type.name == 'choice':
        if stepDB.choice:
            stepDB.choice.labelleft = step.choice.option_left.label
            stepDB.choice.labelright = step.choice.option_right.label
            stepDB.choice.redirectleft = step.choice.option_left.redirect
            stepDB.choice.redirectright = step.choice.option_right.redirect
            await stepDB.choice.save()
        else:
            stepDB.choice = await Models.Choice.create(labelleft=step.choice.option_left.label, labelright=step.choice.option_right.label, redirectleft=step.choice.option_left.redirect, redirectright=step.choice.option_right.redirect)
        await stepDB.save()
    else:
        stepDB.choice = None
        await stepDB.save()
        choice = await Models.Choice.get_or_none(id=stepDB.choice_id)
        if choice:
            await choice.delete()
    # clear all targets
    await stepDB.targets.clear()
    for target in step.targets:
        await stepDB.targets.add(await Models.Target.get(id=target))
    stepDB.position.x = step.position.x
    stepDB.position.y = step.position.y
    stepDB.position.z = step.position.z
    await stepDB.position.save()
    return await stepToJSON(await Models.Step.get(id=idStep).prefetch_related('targets', 'position', 'choice'))


@router.delete('/steps/{idStep}')
async def deleteStep(idStep: int, user: Models.User = Depends(utils.InstructorRequired)):
    await Models.Step.filter(id=idStep).delete()
    return {'ok': 'étape supprimée'}


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
        'ordernumber': step.ordernumber,
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
