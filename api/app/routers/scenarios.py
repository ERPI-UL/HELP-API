from fastapi import APIRouter, Body, Depends, HTTPException, UploadFile, status, File
from fastapi.responses import FileResponse
from pydantic import parse_obj_as
from tortoise.contrib.pydantic import pydantic_model_creator
import Models
import utils
import aiofiles
import aiofiles.os
from tortoise import transactions
router = APIRouter()


# TODO:TRANSLATE SUPPORT
@router.get("/", response_model=Models.pagination,summary="Récupérer la liste des scénarios , avec de la pagination")
async def read_scenarios(idMachine: int = None, page: int = 1, per_page: int = 10,lang:str|None=None,):
    # check for zero per_page
    if per_page == 0:
        per_page = 1
    if idMachine:
        scenario_count = await Models.Scenario.filter(machine=idMachine).count()
        if scenario_count < per_page:
            per_page = scenario_count
        scenarios = await Models.Scenario.filter(machine=idMachine).offset((page - 1) * per_page).limit(per_page).prefetch_related('machine__texts__language','texts','texts__language').order_by('id')
    else:
        scenario_count = await Models.Scenario.all().count()
        if scenario_count < per_page:
            per_page = scenario_count
        scenarios = await Models.Scenario.all().offset((page - 1) * per_page).limit(per_page).prefetch_related('machine__texts__language','texts','texts__language').order_by('id')
    # calculate the number of pages
    lastPage = scenario_count // per_page
    if scenario_count % per_page != 0:
        lastPage += 1
    if(page > lastPage):
        raise HTTPException(status_code=404, detail="Page not found")
    if lang is None:
        lang = "fr"
    language = await Models.Language.get(code=lang)
    for scenario in scenarios:
        for text in scenario.texts:
            if text.language.code == lang:
                scenario.name = text.name
                scenario.description = text.description
        for machineText in scenario.machine.texts:
            if machineText.language.code == lang:
                scenario.machine.name = machineText.name
                scenario.machine.description = machineText.description
    return {
        'total': scenario_count,
        'per_page': per_page,
        'current_page': page,
        'last_page': lastPage,
        'data': [await shortScenarioToJSON(scenario,language) for scenario in scenarios]
    }

@router.put("/{idScenario}",summary="Mettre a jour les informations d'un scenario")
async def update_scenario(idScenario: int, scenario: Models.ScenarioUpdate,lang:str|None=None, user: Models.User = Depends(utils.InstructorRequired)):
    scenarioInDB = await Models.Scenario.get(id=idScenario)
    if lang is None:
        lang = "fr"
    scenarioText = await Models.ScenarioText.get(scenario=scenarioInDB, language__code=lang)
    if(scenario.name.strip() != ""):
        scenarioInDB.name = scenario.name
        scenarioText.name = scenario.name
    if(scenario.description.strip() != ""):
        scenarioInDB.description = scenario.description
        scenarioText.description = scenario.description
    machine = await Models.Machine.get(id=scenario.idMachine)
    scenarioInDB.machine = machine
    await scenarioInDB.save()
    await scenarioText.save()
    return {'ok': "scenario mis à jour"}


@router.delete('/machines/{machine_id}',summary="Supprimer une machine")
async def delete_machine(machine_id: int,lang:str|None=None, user: Models.User = Depends(utils.InstructorRequired)):
    machine = await Models.Machine.get(id=machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine introuvable")
    if lang is None:
        await machine.delete()
    else:
        language = await Models.Language.get(code=lang)
        await Models.MachineText.filter(machine=machine, language=language).delete()
    await machine.delete()
    return {'ok': 'machine supprimée'}

@router.get('/machines', response_model=Models.pagination,summary="Récupérer la liste des machines , avec de la pagination")
async def getMachines(page: int = 1, per_page: int = 10,lang:str|None=None):
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
    if lang is None:
        lang = "fr"
    machines = await Models.Machine.all().offset((page - 1) * per_page).limit(per_page).prefetch_related('texts','texts__language')
    for machine in machines:
        # text = (x for x in machine.texts if machine.texts.language.code == lang)
        # text = next((x for x in machine.texts if machine.texts.language.code == lang), None)
        # print(text)
        # if text:
        #     machine.name = text.name
        #     machine.description = text.description
        for text in machine.texts:
            if text.language.code == lang:
                machine.name = text.name
                machine.description = text.description
    return {
        'total': machine_count,
        'per_page': per_page,
        'current_page': page,
        'last_page': lastPage,
        'data': parse_obj_as(list[Models.MachineOut], machines)
    }

@router.get('/machines/{machine_id}',summary="Récupérer une machine")
async def getMachine(machine_id: int,lang:str|None=None):
    machine = await Models.Machine.get(id=machine_id).prefetch_related('targets')
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    if lang is None:
        lang = "fr"
    language = await Models.Language.get(code=lang)
    text = await Models.MachineText.get(machine=machine, language=language)
    machine.name = text.name
    machine.description = text.description
    return await machineWithTargetsToJSON(machine,language)


@router.get('/machines/{machine_id}/model', response_class=FileResponse,summary="Récupérer le modèle 3D de la machine au format GLTF Binaire .glb")
async def getMachineModel(machine_id: int):
    machine = await Models.Machine.get(id=machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine introuvable")
    try:
        # test if file exists
        await aiofiles.os.stat(machine.path)
        return FileResponse(
            machine.path, media_type='application/octet-stream', filename=machine.name+'.glb')  # FastApi will automatically find the file and return it
    except Exception:
        raise HTTPException(status_code=404, detail="Model introuvable")


@router.post('/machines/{machine_id}/model',summary="Envoyer le modèle 3D de la machine au format GLTF Binaire .glb")
async def postMachineModel(machine_id: int, model: UploadFile = File(...), user: Models.User = Depends(utils.InstructorRequired)):
    machine = await Models.Machine.get(id=machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine introuvable")
    machine.path = utils.MODELS_DIRECTORY+str(machine.id)+"/machine.fbx"
    async with transactions.in_transaction() as connection:
        try:
            contents = await model.read()
            # create the directory if it doesn't exist
            await aiofiles.os.makedirs(utils.MODELS_DIRECTORY+str(machine.id), exist_ok=True)
            async with aiofiles.open(machine.path, 'wb') as f:
                await f.write(contents)
            await machine.save()
        except Exception:
            connection.rollback()
            raise HTTPException(
                status_code=500, detail="Erreur lors de l'enregistrement du fichier")
        finally:
            await model.close()

    return {"ok": f" fichier envoyé : {model.filename}"}


@router.post('/machines/{machine_id}/targets', response_model=Models.TargetOut,summary="Ajouter une cible à une machine")
async def createTarget(machine_id: int, name: str = Body(..., embed=True), user: Models.User = Depends(utils.InstructorRequired)):
    machine = await Models.Machine.get(id=machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine introuvable")
    target = Models.Target(name=name, machine=machine)
    await target.save()
    return parse_obj_as(Models.TargetOut, target)
@router.get('/machines/{machine_id}/languages',response_model=list[Models.LanguageOut],summary="Récupérer les langues disponibles pour une machine")
async def getMachineLanguages(machine_id: int):
    texts = await Models.MachineText.filter(machine_id=machine_id).prefetch_related('language')
    return [parse_obj_as(Models.LanguageOut, text.language) for text in texts]

@router.delete('/machines/targets/{target_id}',summary="Supprimer une cible")
async def deleteTarget(target_id: int, user: Models.User = Depends(utils.InstructorRequired)):
    target = await Models.Target.get(id=target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target introuvable")
    await target.delete()
    return {'ok': 'target supprimée'}


@router.put('/machines/targets/{target_id}',summary="Mettre à jour une cible")
async def updateTarget(target_id: int, target: Models.TargetPost, user: Models.User = Depends(utils.InstructorRequired)):
    targetInDB = await Models.Target.get(id=target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Cible introuvable")
    targetInDB.name = target.name
    await targetInDB.save()
    return {'ok': 'Cible mise à jour'}

@router.get('/{idScenario}',summary="Récupère un scénario sous forme de JSON")
async def getScenario(idScenario: int,lang:str|None=None):
    scenario = await Models.Scenario.get(id=idScenario).prefetch_related('steps__targets', 'steps__position', 'steps__choice','steps__type','machine')
    # scenario2 = await Models.Scenario.get(id=id).values('id', 'name', 'description', 'steps__id', 'steps__label', 'steps__name', 'steps__description')
    if lang is None:
        lang = "fr"
    language = await Models.Language.get(code=lang)
    scenarioText = await Models.ScenarioText.get(scenario=scenario, language=language)
    scenario.name = scenarioText.name
    scenario.description = scenarioText.description
    for step in scenario.steps:
        stepText = await Models.StepText.get(step=step, language=language)
        step.label = stepText.label
        step.description = stepText.description
        if step.type.name == "choice":
            choiceText = await Models.ChoiceText.get(choice=step.choice, language=language)
            step.choice.labelleft = choiceText.labelleft
            step.choice.labelright = choiceText.labelright
            step.choice.redirectleft = choiceText.redirectleft
            step.choice.redirectright = choiceText.redirectright
    machineText = await Models.MachineText.get(machine=scenario.machine, language=language)
    scenario.machine.name = machineText.name
    scenario.machine.description = machineText.description
    return await scenarioToJSON(scenario,language)

@router.get("/{idScenario}/languages", summary="Récupère les langues disponibles pour un scénario")
async def getScenarioLanguages(idScenario: int):
    texts = await Models.ScenarioText.filter(scenario_id=idScenario).prefetch_related('language')
    return [parse_obj_as(Models.LanguageOut, text.language) for text in texts]

@router.delete('/{idScenario}',summary="Supprimer un scénario")
@transactions.atomic()
async def delete_scenario(idScenario: int,lang:str|None=None, user: Models.User = Depends(utils.InstructorRequired)):
    scenario = await Models.Scenario.get(id=idScenario)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario introuvable")
    # on différentie la suppression du scénario d'une traduction du scenario
    if lang is None:
        await scenario.delete()
    else:
        language = await Models.Language.get(code=lang)
        await Models.ScenarioText.filter(scenario_id=idScenario,language=language).delete()
        await Models.StepText.filter(step__scenario_id=idScenario,language=language).delete()
        await Models.ChoiceText.filter(choice__step__scenario_id=idScenario,language=language).delete()
    return {'ok': 'scenario et objets référencés supprimés'}

@router.post("/machines",summary="Créer une machine")
@transactions.atomic()
async def create_machine(machine: Models.Machinein,lang:str, adminLevel: int = Depends(utils.getAdminLevel)):
    if adminLevel < utils.Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if lang is None:
        lang = "fr"
    language = await Models.Language.get(code=lang)
    machineDB = await Models.Machine.create(name=machine.name, description=machine.description)
    await Models.MachineText.create(machine=machineDB, language=language, name=machine.name, description=machine.description)
    return await Models.MachineOut.from_tortoise_orm(machineDB)

@router.put('/machines/{idMachine}',summary="Mettre à jour une machine")
async def update_machine(idMachine: int, machine: Models.Machinein,lang:str|None=None, adminLevel: int = Depends(utils.getAdminLevel)):
    if adminLevel < utils.Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough rights")
    if lang is None:
        lang = "fr"
    machineDB = await Models.Machine.get(id=idMachine)
    machineDB.name = machine.name
    machineDB.description = machine.description
    await machineDB.save()
    await Models.MachineText.filter(machine_id=machineDB.id,language_code=lang).update(name=machine.name, description=machine.description)
    return await Models.Machinein.from_tortoise_orm(await Models.Machine.get(id=idMachine))


@router.post('/',summary="Créer un scénario dans la base de données depuis un JSON")
@transactions.atomic()
async def createScenario(scenario: Models.ScenarioPost,lang:str|None=None, adminLevel: int = Depends(utils.getAdminLevel)):
    if lang is None:
        lang = "fr"
    if adminLevel < utils.Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough rights")
    language = await Models.Language.get(code=lang)
    scenarioDB = await Models.Scenario.create(name=scenario.name, description=scenario.description, machine=await Models.Machine.get(id=scenario.machine.id))
    await Models.ScenarioText.create(scenario_id=scenarioDB.id, language=language, name=scenario.name, description=scenario.description)
    for step in scenario.steps:
        position = await Models.Position.create(x=step.position.x, y=step.position.y, z=step.position.z)
        type = await Models.Type.get(name=step.type.name).first()
        stepDB = Models.Step(scenario=scenarioDB, type=type, label=step.label, position=position,
                             name=step.name, description=step.description, ordernumber=step.ordernumber)
        if step.type.name == 'choice':
            stepDB.choice = await Models.Choice.create(labelleft=step.choice.option_left.label, labelright=step.choice.option_right.label, redirectleft=step.choice.option_left.redirect, redirectright=step.choice.option_right.redirect)
            await Models.ChoiceText.create(choice_id=stepDB.choice.id, language=language, labelleft=step.choice.option_left.label, labelright=step.choice.option_right.label,redirectleft=step.choice.option_left.redirect, redirectright=step.choice.option_right.redirect)
        await stepDB.save()
        await Models.StepText.create(step_id=stepDB.id, language=language, label=step.label, description=step.description)
        for target in step.targets:
            await stepDB.targets.add(await Models.Target.get(id=target))
    return {'id': scenarioDB.id}

@router.post('/{idScenario}/steps',summary="Ajoute une nouvelle étape au scénario")
@transactions.atomic()
async def createStep(idScenario: int, step: Models.StepPost,lang:str|None=None, adminLevel: int = Depends(utils.getAdminLevel)):
    if adminLevel < utils.Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough rights")
    if lang is None:
        lang = "fr"
    language = await Models.Language.get(code=lang)
    scenario = await Models.Scenario.get(id=idScenario)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario introuvable")
    position = await Models.Position.create(x=step.position.x, y=step.position.y, z=step.position.z)
    type = await Models.Type.get(name=step.type.name).first()
    stepDB = Models.Step(scenario=scenario, type=type, label=step.label, position=position,
                         name=step.name, description=step.description, ordernumber=step.ordernumber)
    if step.type.name == 'choice':
        stepDB.choice = await Models.Choice.create(labelleft=step.choice.option_left.label, labelright=step.choice.option_right.label, redirectleft=step.choice.option_left.redirect, redirectright=step.choice.option_right.redirect)
        await Models.ChoiceText.create(choice_id=stepDB.choice.id, language=language, labelleft=step.choice.option_left.label, labelright=step.choice.option_right.label,redirectleft=step.choice.option_left.redirect, redirectright=step.choice.option_right.redirect)
    await stepDB.save()
    await Models.StepText.create(step_id=stepDB.id, language=language, label=step.label, description=step.description)
    for target in step.targets:
        await stepDB.targets.add(await Models.Target.get(id=target))
    return {'id': stepDB.id}

@router.put('/steps/{idStep}',summary="Met à jour une étape du scénario")
@transactions.atomic()
async def updateStep(idStep: int, step: Models.StepPost,lang:str|None=None, adminLevel: int = Depends(utils.getAdminLevel)):
    if adminLevel < utils.Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough rights")
    stepDB = await Models.Step.get(id=idStep).prefetch_related('targets', 'position', 'choice')
    if not stepDB:
        raise HTTPException(status_code=404, detail="Step introuvable")
    if lang is None:
        lang = "fr"
    language = await Models.Language.get(code=lang)
    stepDB.label = step.label
    stepDB.name = step.name
    stepDB.description = step.description
    stepDB.ordernumber = step.ordernumber
    stepDB.type = await Models.Type.get(name=step.type.name).first()
    stepTextDB = await Models.StepText.get(step_id=stepDB.id, language=language)
    stepTextDB.label = step.label
    stepTextDB.description = step.description
    await stepTextDB.save()
    if step.type.name == 'choice':
        if stepDB.choice:
            stepDB.choice.labelleft = step.choice.option_left.label
            stepDB.choice.labelright = step.choice.option_right.label
            stepDB.choice.redirectleft = step.choice.option_left.redirect
            stepDB.choice.redirectright = step.choice.option_right.redirect
            await stepDB.choice.save()
            choiceTextDB = await Models.ChoiceText.get(choice_id=stepDB.choice.id, language=language)
            choiceTextDB.labelleft = step.choice.option_left.label
            choiceTextDB.labelright = step.choice.option_right.label
            choiceTextDB.redirectleft = step.choice.option_left.redirect
            choiceTextDB.redirectright = step.choice.option_right.redirect
            await choiceTextDB.save()
        else:
            stepDB.choice = await Models.Choice.create(labelleft=step.choice.option_left.label, labelright=step.choice.option_right.label, redirectleft=step.choice.option_left.redirect, redirectright=step.choice.option_right.redirect)
            await Models.ChoiceText.create(choice_id=stepDB.choice.id, language=language, labelleft=step.choice.option_left.label, labelright=step.choice.option_right.label,redirectleft=step.choice.option_left.redirect, redirectright=step.choice.option_right.redirect)
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
    return await stepToJSON(await Models.Step.get(id=idStep).prefetch_related('targets', 'position', 'choice', 'type'))


@router.delete('/steps/{idStep}',summary="Supprime une étape du scénario")
async def deleteStep(idStep: int,lang:str|None=None, user: Models.User = Depends(utils.InstructorRequired)):
    if lang is None:
        await Models.Step.filter(id=idStep).delete()
    else:
        language = await Models.Language.get(code=lang)
        await Models.StepText.filter(step_id=idStep, language=language).delete()
    return {'ok': 'étape supprimée'}


async def scenarioToJSON(scenario,language=None):
    return {
        'id': scenario.id,
        'name': scenario.name,
        'description': scenario.description,
        'language': language.code if language else None,
        'machine': await machineToJSON(scenario.machine,language),
        'steps': [await stepToJSON(step) for step in scenario.steps]
    }


async def shortScenarioToJSON(scenario,language=None):
    return {
        'id': scenario.id,
        'name': scenario.name,
        'description': scenario.description,
        'language': language.code if language else None,
        'machine': await machineToJSON(scenario.machine,language)
    }


async def stepToJSON(step):
    return {
        'id': step.id,
        'ordernumber': step.ordernumber,
        'description': step.description,
        'label': step.label,
        'name': step.name,
        'position': await positionToJSON(step.position),
        'type': step.type.name,
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


async def machineToJSON(machine,language=None):
    return {
        'id': machine.id,
        'name': machine.name,
        'description': machine.description,
        'language': language.code if language else None,
    }


async def positionToJSON(position: Models.Position):
    if not position:
        return None
    return {'x': position.x, 'y': position.y, 'z': position.z}


async def machineWithTargetsToJSON(machine,language=None):
    targets = []
    for target in machine.targets:
        targets.append({'id': target.id, 'name': target.name})
    return {
        'id': machine.id,
        'name': machine.name,
        'description': machine.description,
        'language': language.code if language else None,
        'targets': targets
    }
