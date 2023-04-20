import hashlib

import aiofiles
import aiofiles.os
from aioshutil import rmtree
from fastapi import (APIRouter, Body, Depends, File, HTTPException, UploadFile,
                     status)
from fastapi.responses import FileResponse
from pydantic import parse_obj_as
from tortoise import transactions

from app.models import (Choice, ChoiceText, IDResponse, Language, LanguageOut,
                        Machine, Machinein, MachineOut, MachineText,
                        Pagination, Position, Scenario, ScenarioPost,
                        ScenarioText, ScenarioUpdate, Step, StepPost, StepText,
                        Target, TargetOut, TargetPost, Type)
from app.utils import (MODELS_DIRECTORY, SCENARIOS_DATA_DIRECTORY, Permission,
                       get_admin_level, insctructor_required)

router = APIRouter()


# TODO:TRANSLATE SUPPORT
@router.get("/", response_model=Pagination, summary="Récupérer la liste des scénarios , avec de la pagination")
async def read_scenarios(id_machine: int = None, page: int = 1, per_page: int = 10, lang: str | None = None,):
    """ Returns a list of scenarios with pagination and machine filter"""
    # check for zero per_page
    if per_page == 0:
        per_page = 1
    if id_machine:
        scenario_count = await Scenario.filter(machine=id_machine).count()
        if scenario_count < per_page:
            per_page = scenario_count
        scenarios = await Scenario.filter(machine=id_machine).offset((page - 1) * per_page)\
            .limit(per_page).prefetch_related('machine__texts__language', 'texts', 'texts__language').order_by('id')
    else:
        scenario_count = await Scenario.all().count()
        if scenario_count < per_page:
            per_page = scenario_count
        scenarios = await Scenario.all().offset((page - 1) * per_page).limit(per_page)\
            .prefetch_related('machine__texts__language', 'texts', 'texts__language').order_by('id')
    # check for zero per_page
    if per_page == 0:
        per_page = 1
    # calculate the number of pages
    last_page = scenario_count // per_page
    if scenario_count % per_page != 0:
        last_page += 1
    if page > last_page:
        raise HTTPException(status_code=404, detail="Page not found")
    if lang is None:
        lang = "fr"
    language = await Language.get(code=lang)
    for scenario in scenarios:
        for text in scenario.texts:
            if text.language.code == lang:
                scenario.name = text.name
                scenario.description = text.description
        for machine_text in scenario.machine.texts:
            if machine_text.language.code == lang:
                scenario.machine.name = machine_text.name
                scenario.machine.description = machine_text.description
    return {
        'total': scenario_count,
        'per_page': per_page,
        'current_page': page,
        'last_page': last_page,
        'data': [await short_scenario_to_json(scenario, language) for scenario in scenarios]
    }


@router.put("/{id_scenario}", summary="Mettre a jour les informations d'un scenario")
async def update_scenario(id_scenario: int, scenario: ScenarioUpdate, lang: str | None = None, _=Depends(insctructor_required)):
    """ Update a scenario by id"""
    scenario_in_db = await Scenario.get(id=id_scenario)
    if lang is None:
        lang = "fr"
    scenario_text = await ScenarioText.get(scenario=scenario_in_db, language__code=lang)
    if scenario.name.strip() != "":
        scenario_in_db.name = scenario.name
        scenario_text.name = scenario.name
    if scenario.description.strip() != "":
        scenario_in_db.description = scenario.description
        scenario_text.description = scenario.description
    machine = await Machine.get(id=scenario.idMachine)
    scenario_in_db.machine = machine
    await scenario_in_db.save()
    await scenario_text.save()
    return {'ok': "scenario mis à jour"}


@router.delete('/machines/{machine_id}', summary="Supprimer une machine")
async def delete_machine(machine_id: int, lang: str | None = None, _=Depends(insctructor_required)):
    """ Delete a machine by id"""
    machine = await Machine.get(id=machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine introuvable")
    if lang is None:
        await machine.delete()
    else:
        language = await Language.get(code=lang)
        await MachineText.filter(machine=machine, language=language).delete()
    await machine.delete()
    return {'ok': 'machine supprimée'}


@router.get('/machines', response_model=Pagination, summary="Récupérer la liste des machines , avec de la pagination")
async def get_machines(page: int = 1, per_page: int = 10, lang: str | None = None):
    """ Returns a list of machines with pagination"""
    machine_count = await Machine.all().count()
    if machine_count < per_page:
        per_page = machine_count
    # check for zero per_page
    if per_page == 0:
        per_page = 1
    # calculate the number of pages
    last_page = machine_count // per_page
    if machine_count % per_page != 0:
        last_page += 1
    if page > last_page:
        raise HTTPException(status_code=404, detail="Page non trouvée")
    if lang is None:
        lang = "fr"
    machines = await Machine.all().offset((page - 1) * per_page).limit(per_page).prefetch_related('texts', 'texts__language')
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
        'last_page': last_page,
        'data': parse_obj_as(list[MachineOut], machines)
    }


@router.get('/machines/{machine_id}', summary="Récupérer une machine")
async def get_machine(machine_id: int, lang: str | None = None):
    """ Returns a machine by id"""
    machine = await Machine.get(id=machine_id).prefetch_related('targets')
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    if lang is None:
        lang = "fr"
    language = await Language.get(code=lang)
    text = await MachineText.get(machine=machine, language=language)
    machine.name = text.name
    machine.description = text.description
    return await machine_with_targets_to_json(machine, language)


@router.get('/machines/{machine_id}/model', response_class=FileResponse, summary="Récupérer le modèle 3D de la machine au format GLTF Binaire .glb")
async def get_machine_model(machine_id: int):
    """ Returns a machine model in glb format by id"""
    machine = await Machine.get(id=machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine introuvable")
    try:
        # test if file exists
        await aiofiles.os.stat(machine.path)
        # FastApi will automatically find the file and return it
        return FileResponse(machine.path, media_type='application/octet-stream', filename=machine.name+'.glb')
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Model introuvable") from exc


@router.post('/machines/{machine_id}/model', summary="Envoyer le modèle 3D de la machine au format GLTF Binaire .glb")
async def post_machine_model(machine_id: int, model: UploadFile = File(...), _=Depends(insctructor_required)):
    """ Upload a machine model in glb format by id"""
    machine = await Machine.get(id=machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine introuvable")
    machine.path = MODELS_DIRECTORY+str(machine.id)+"/machine.glb"
    async with transactions.in_transaction() as connection:
        try:
            contents = await model.read()
            # create the directory if it doesn't exist
            await aiofiles.os.makedirs(MODELS_DIRECTORY+str(machine.id), exist_ok=True)
            async with aiofiles.open(machine.path, 'wb') as file:
                await file.write(contents)
            await machine.save()
        except Exception as exc:
            connection.rollback()
            raise HTTPException(
                status_code=500, detail="Erreur lors de l'enregistrement du fichier") from exc
        finally:
            await model.close()

    return {"ok": f" fichier envoyé : {model.filename}"}


@router.post('/machines/{machine_id}/targets', response_model=TargetOut, summary="Ajouter une cible à une machine")
async def create_target(machine_id: int, name: str = Body(..., embed=True), _=Depends(insctructor_required)):
    """ Create a target for a machine by id """
    machine = await Machine.get(id=machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine introuvable")
    target = Target(name=name, machine=machine)
    await target.save()
    return parse_obj_as(TargetOut, target)


@router.get('/machines/{machine_id}/languages', response_model=list[LanguageOut], summary="Récupérer les langues disponibles pour une machine")
async def get_machine_languages(machine_id: int):
    """ Returns a list of languages for a machine by id"""
    texts = await MachineText.filter(machine_id=machine_id).prefetch_related('language')
    return [parse_obj_as(LanguageOut, text.language) for text in texts]


@router.delete('/machines/targets/{target_id}', summary="Supprimer une cible")
async def delete_target(target_id: int, _=Depends(insctructor_required)):
    """ Delete a target by id"""
    target = await Target.get(id=target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target introuvable")
    await target.delete()
    return {'ok': 'target supprimée'}


@router.put('/machines/targets/{target_id}', summary="Mettre à jour une cible")
async def update_target(target_id: int, target: TargetPost, _=Depends(insctructor_required)):
    """ Update a target by id"""
    target_in_db = await Target.get(id=target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Cible introuvable")
    target_in_db.name = target.name
    await target_in_db.save()
    return {'ok': 'Cible mise à jour'}


@router.get('/{id_scenario}', summary="Récupère un scénario sous forme de JSON")
async def get_scenario(id_scenario: int, lang: str | None = None):
    """ Returns a scenario by id"""
    scenario = await Scenario.get(id=id_scenario).prefetch_related('steps__targets', 'steps__position', 'steps__choice', 'steps__type', 'machine')
    # scenario2 = await Scenario.get(id=id).values('id', 'name', 'description', 'steps__id', 'steps__label', 'steps__name', 'steps__description')
    if lang is None:
        lang = "fr"
    language = await Language.get(code=lang)
    scenario_text = await ScenarioText.get(scenario=scenario, language=language)
    scenario.name = scenario_text.name
    scenario.description = scenario_text.description
    for step in scenario.steps:
        step_text = await StepText.get(step=step, language=language)
        step.label = step_text.label
        step.description = step_text.description
        if step.type.name == "choice":
            choice_text = await ChoiceText.get(choice=step.choice, language=language)
            step.choice.labelleft = choice_text.labelleft
            step.choice.labelright = choice_text.labelright
            step.choice.redirectleft = choice_text.redirectleft
            step.choice.redirectright = choice_text.redirectright
    machine_text = await MachineText.get_or_none(machine=scenario.machine, language=language)
    if not machine_text:
        machine_text = await MachineText.filter(machine=scenario.machine).first()
    scenario.machine.name = machine_text.name
    scenario.machine.description = machine_text.description
    return await scenario_to_json(scenario, language)


@router.get("/{id_scenario}/languages", summary="Récupère les langues disponibles pour un scénario")
async def get_scenario_languages(id_scenario: int):
    """Retrieve the languages available for a scenario"""
    texts = await ScenarioText.filter(scenario_id=id_scenario).prefetch_related('language')
    return [parse_obj_as(LanguageOut, text.language) for text in texts]


@router.delete('/{id_scenario}', summary="Supprimer un scénario")
@transactions.atomic()
async def delete_scenario(id_scenario: int, lang: str | None = None, _=Depends(insctructor_required)):
    """ Delete a scenario and all the objects related to it in a specific language"""
    scenario = await Scenario.get(id=id_scenario).prefetch_related('steps')
    path = SCENARIOS_DATA_DIRECTORY + str(scenario.id)
    if await aiofiles.os.path.exists(path):
        try:
            await rmtree(path)
        except Exception as exc:
            print(exc)
            raise HTTPException(
                status_code=500, detail="Erreur lors de la suppression du fichier") from exc
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario introuvable")
    # on différentie la suppression du scénario d'une traduction du scenario
    if lang is None:
        await scenario.delete()
    else:
        language = await Language.get(code=lang)
        await ScenarioText.filter(scenario_id=id_scenario, language=language).delete()
        await StepText.filter(step__scenario_id=id_scenario, language=language).delete()
        await ChoiceText.filter(choice__step__scenario_id=id_scenario, language=language).delete()
    return {'ok': 'scenario et objets référencés supprimés'}


@router.post("/machines", summary="Créer une machine")
@transactions.atomic()
async def create_machine(machine: Machinein, lang: str | None = None, admin_level: int = Depends(get_admin_level)):
    """ Create a machine and a translation for it in a specific language"""
    if admin_level < Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if lang is None:
        lang = "fr"
    language = await Language.get(code=lang)
    machine_db = await Machine.create(name=machine.name, description=machine.description)
    await MachineText.create(machine=machine_db, language=language, name=machine.name, description=machine.description)
    return await MachineOut.from_tortoise_orm(machine_db)


@router.put('/machines/{id_machine}', summary="Mettre à jour une machine")
async def update_machine(id_machine: int, machine: Machinein, lang: str | None = None, admin_level: int = Depends(get_admin_level)):
    """ Update a machine and a translation for it in a specific language"""
    if admin_level < Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough rights")
    if lang is None:
        lang = "fr"
    machine_db = await Machine.get(id=id_machine)
    machine_db.name = machine.name
    machine_db.description = machine.description
    await machine_db.save()
    await MachineText.filter(machine_id=machine_db.id, language_code=lang).update(name=machine.name, description=machine.description)
    return await Machinein.from_tortoise_orm(await Machine.get(id=id_machine))


@router.post('/', summary="Créer un scénario dans la base de données depuis un JSON", response_model=IDResponse)
@transactions.atomic()
async def create_scenario(scenario: ScenarioPost, lang: str | None = None, admin_level: int = Depends(get_admin_level)):
    """ Create a scenario and a translation for it in a specific language"""
    if lang is None:
        lang = "fr"
    if admin_level < Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough rights")
    language = await Language.get(code=lang)
    scenario_in_db = await Scenario.create(name=scenario.name, description=scenario.description, machine=await Machine.get(id=scenario.machine.id))
    await ScenarioText.create(scenario_id=scenario_in_db.id, language=language, name=scenario.name, description=scenario.description)
    for step in scenario.steps:
        position = await Position.create(x=step.position.x, y=step.position.y, z=step.position.z)
        type_in_db = await Type.get(name=step.type.name).first()
        step_db: Step = Step(scenario=scenario_in_db, type=type_in_db, label=step.label, position=position,
                             name=step.name, description=step.description, ordernumber=step.ordernumber)
        if step.type.name == 'choice':
            step_db.choice = await Choice.create(labelleft=step.choice.option_left.label, labelright=step.choice.option_right.label,
                                                 redirectleft=step.choice.option_left.redirect, redirectright=step.choice.option_right.redirect)
            await ChoiceText.create(choice_id=step_db.choice.id, language=language, labelleft=step.choice.option_left.label,
                                    labelright=step.choice.option_right.label, redirectleft=step.choice.option_left.redirect,
                                    redirectright=step.choice.option_right.redirect)
        await step_db.save()
        await StepText.create(step_id=step_db.id, language=language, label=step.label, description=step.description)
        for target in step.targets:
            await step_db.targets.add(await Target.get(id=target))
    return {'id': scenario_in_db.id}


@router.post('/{id_scenario}/steps', summary="Ajoute une nouvelle étape au scénario", response_model=IDResponse)
@transactions.atomic()
async def create_step(id_scenario: int, step: StepPost, lang: str | None = None, admin_level: int = Depends(get_admin_level)):
    """ Create a step and a translation for it in a specific language"""
    if admin_level < Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough rights")
    if lang is None:
        lang = "fr"
    language = await Language.get(code=lang)
    scenario = await Scenario.get(id=id_scenario)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario introuvable")
    position = await Position.create(x=step.position.x, y=step.position.y, z=step.position.z)
    type_in_db = await Type.get(name=step.type.name).first()
    step_in_db = Step(scenario=scenario, type=type_in_db, label=step.label, position=position,
                      name=step.name, description=step.description, ordernumber=step.ordernumber)
    if step.type.name == 'choice':
        step_in_db.choice = await Choice.create(labelleft=step.choice.option_left.label, labelright=step.choice.option_right.label,
                                                redirectleft=step.choice.option_left.redirect, redirectright=step.choice.option_right.redirect)
        await ChoiceText.create(choice_id=step_in_db.choice.id, language=language, labelleft=step.choice.option_left.label,
                                labelright=step.choice.option_right.label, redirectleft=step.choice.option_left.redirect,
                                redirectright=step.choice.option_right.redirect)
    await step_in_db.save()
    await StepText.create(step_id=step_in_db.id, language=language, label=step.label, description=step.description)
    for target in step.targets if step.targets else []:
        await step_in_db.targets.add(await Target.get(id=target))
    return {'id': step_in_db.id}


@router.post('/{id_scenario}/steps/{id_step}/ressource', summary="Ajouter ou remplacer la ressource associer à une étape",
             description="Une étape peut avoir une ressource de type vidéo ou image. Cette dernière sera affiché lors de l'éxécution de l'étape")
@transactions.atomic()
async def add_ressource_to_a_step(id_scenario: int, id_step: int, ressource_file: UploadFile, _: int = Depends(insctructor_required)):
    """ Add a ressource to a step """
    scenario = await Scenario.get_or_none(id=id_scenario)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario introuvable")
    step = await Step.get_or_none(id=id_step).prefetch_related('scenario')
    if not step:
        raise HTTPException(status_code=404, detail="Etape introuvable")
    if step.scenario.id != id_scenario:
        raise HTTPException(status_code=404, detail="Cette étape ne correspond pas à ce scenario")
    extension = ressource_file.filename.split(".")[-1]
    # verify that the file is an image or a video
    if extension not in ["png", "jpg", "jpeg", "gif", "mp4", "pdf"]:
        raise HTTPException(
            status_code=415, detail="Unsupported media type")
    content = await ressource_file.read()
    # verify that the size does not exceed 4 Mio
    if len(content) > 4*1024*1024:
        raise HTTPException(
            status_code=413, detail="File too large")
    hash_value = hashlib.sha256(content).hexdigest()
    # create the directory if it doesn't exist
    path = SCENARIOS_DATA_DIRECTORY+str(scenario.id)+'/ressources'
    await aiofiles.os.makedirs(path, exist_ok=True)
    async with aiofiles.open(f"{path}/{hash_value}.{extension}", 'wb') as file:
        await file.write(content)
    if step.ressourcePath is not None:
        # remove the old file
        await aiofiles.os.remove(f"{path}/{step.ressourcePath}")
    step.ressourcePath = f"{hash_value}.{extension}"
    await step.save()
    return {'ok': f"Ressource {ressource_file.filename} ajoutée à l'étape {step.id}"}


@router.delete('steps/{id_step}/ressource', summary="Supprime la ressource associée à une étape",
               description="Cette route permet de supprimer la ressource mais de garder l'étape")
@transactions.atomic()
async def delete_ressource_of_a_step(id_step: int, _: int = Depends(insctructor_required)):
    """ Delete a ressource to a step """
    step = await Step.get_or_none(id=id_step).prefetch_related('scenario')
    if not step:
        raise HTTPException(status_code=404, detail="Etape introuvable")
    if step.ressourcePath is not None:
        # remove the old file
        path = SCENARIOS_DATA_DIRECTORY+str(step.scenario.id)+'/ressources'
        try:
            await aiofiles.os.remove(f"{path}/{step.ressourcePath}")
            step.ressourcePath = None
            await step.save()
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="Ressource introuvable") from exc
    return {'ok': f"Ressource de l'étape {step.id} supprimée"}


@router.put('/steps/{id_step}', summary="Met à jour une étape du scénario")
@transactions.atomic()
async def update_step(id_step: int, step: StepPost, lang: str | None = None, admin_level: int = Depends(get_admin_level)):
    """ Update a step and a translation for it in a specific language"""
    if admin_level < Permission.INSTRUCTOR.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough rights")
    step_in_db = await Step.get(id=id_step).prefetch_related('targets', 'position', 'choice')
    if not step_in_db:
        raise HTTPException(status_code=404, detail="Step introuvable")
    if lang is None:
        lang = "fr"
    language = await Language.get(code=lang)
    step_in_db.label = step.label
    step_in_db.name = step.name
    step_in_db.description = step.description
    step_in_db.ordernumber = step.ordernumber
    step_in_db.type = await Type.get(name=step.type.name).first()
    step_text_in_db = await StepText.get(step_id=step_in_db.id, language=language)
    step_text_in_db.label = step.label
    step_text_in_db.description = step.description
    await step_text_in_db.save()
    if step.type.name == 'choice':
        if step_in_db.choice:
            step_in_db.choice.labelleft = step.choice.option_left.label
            step_in_db.choice.labelright = step.choice.option_right.label
            step_in_db.choice.redirectleft = step.choice.option_left.redirect
            step_in_db.choice.redirectright = step.choice.option_right.redirect
            await step_in_db.choice.save()
            choice_text_in_db = await ChoiceText.get(choice_id=step_in_db.choice.id, language=language)
            choice_text_in_db.labelleft = step.choice.option_left.label
            choice_text_in_db.labelright = step.choice.option_right.label
            choice_text_in_db.redirectleft = step.choice.option_left.redirect
            choice_text_in_db.redirectright = step.choice.option_right.redirect
            await choice_text_in_db.save()
        else:
            step_in_db.choice = await Choice.create(labelleft=step.choice.option_left.label,
                                                    labelright=step.choice.option_right.label,
                                                    redirectleft=step.choice.option_left.redirect,
                                                    redirectright=step.choice.option_right.redirect)
            await ChoiceText.create(choice_id=step_in_db.choice.id, language=language,
                                    labelleft=step.choice.option_left.label,
                                    labelright=step.choice.option_right.label,
                                    redirectleft=step.choice.option_left.redirect,
                                    redirectright=step.choice.option_right.redirect)
        await step_in_db.save()
    else:
        step_in_db.choice = None
        await step_in_db.save()
        choice = await Choice.get_or_none(id=step_in_db.choice_id)
        if choice:
            await choice.delete()
    # clear all targets
    await step_in_db.targets.clear()
    for target in step.targets:
        await step_in_db.targets.add(await Target.get(id=target))
    step_in_db.position.x = step.position.x
    step_in_db.position.y = step.position.y
    step_in_db.position.z = step.position.z
    await step_in_db.position.save()
    return await step_to_json(await Step.get(id=id_step).prefetch_related('targets', 'position', 'choice', 'type'))


@router.delete('/steps/{id_step}', summary="Supprime une étape du scénario")
async def delete_step(id_step: int, lang: str | None = None, _=Depends(insctructor_required)):
    """
    Delete a step from a scenario. If lang is None,
    delete the step and all its translations.
    Otherwise, delete only the translation in the given language.
    """
    if lang is None:
        step = await Step.get(id=id_step).prefetch_related('scenario')
        if step.ressourcePath:
            path = SCENARIOS_DATA_DIRECTORY+str(step.scenario.id)+'/ressources'
            if await aiofiles.os.path.exists(f"{path}/{step.ressourcePath}"):
                await aiofiles.os.remove(f"{path}/{step.ressourcePath}")
        await step.delete()
    else:
        language = await Language.get(code=lang)
        await StepText.filter(step_id=id_step, language=language).delete()
    return {'ok': 'étape supprimée'}


async def scenario_to_json(scenario, language=None):
    """Return a JSON representation of a scenario, with steps"""
    return {
        'id': scenario.id,
        'name': scenario.name,
        'description': scenario.description,
        'language': language.code if language else None,
        'machine': await machine_to_json(scenario.machine, language),
        'steps': [await step_to_json(step) for step in scenario.steps]
    }


async def short_scenario_to_json(scenario, language=None):
    """Return a JSON representation of a scenario, without steps"""
    return {
        'id': scenario.id,
        'name': scenario.name,
        'description': scenario.description,
        'language': language.code if language else None,
        'machine': await machine_to_json(scenario.machine, language)
    }


async def step_to_json(step):
    """Return a JSON representation of a step"""
    return {
        'id': step.id,
        'ordernumber': step.ordernumber,
        'description': step.description,
        'label': step.label,
        'name': step.name,
        'ressource': step.ressourcePath,
        'position': await position_to_json(step.position),
        'type': step.type.name,
        'choice': await choice_to_json(step.choice),
        'targets': [await target_to_json(target) for target in step.targets]
    }


async def target_to_json(target):
    """Return a JSON representation of a target"""
    return {
        'id': target.id,
        'name': target.name,
    }


async def choice_to_json(choice: Choice):
    """Return a JSON representation of a choice"""
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


async def machine_to_json(machine, language=None):
    """Return a JSON representation of a machine"""
    return {
        'id': machine.id,
        'name': machine.name,
        'description': machine.description,
        'language': language.code if language else None,
    }


async def position_to_json(position: Position):
    """Return a JSON representation of a position"""
    if not position:
        return None
    return {'x': position.x, 'y': position.y, 'z': position.z}


async def machine_with_targets_to_json(machine, language=None):
    """Return a JSON representation of a machine with targets"""
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
