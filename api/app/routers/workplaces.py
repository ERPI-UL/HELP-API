from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from fastapi_pagination import Page
from fastapi_pagination.ext.tortoise import paginate
from tortoise.transactions import atomic

from app.models.language import Language
from app.models.workplace import (ArtifactInstance, ArtifactInstanceIn,
                                  ArtifactInstanceInPatch, ArtifactInstanceOut,
                                  Position, WorkPlace, WorkplaceIn,
                                  WorkplaceInPatch, WorkplaceOut,
                                  WorkplaceOutShort, WorkPlaceText)
from app.routers.activities import get_ask_translation_or_first
from app.types.anchor import Anchor
from app.types.response import IDResponse, OKResponse
from app.utils import insctructor_required

router = APIRouter()


@router.get("/", response_model=Page)
async def get_workplaces(language_code: str = "fr"):
    """ get all workplaces """
    pagination = await paginate(WorkPlace.all().prefetch_related("texts", "texts__language").order_by("id"))
    pagination.items = [WorkplaceOutShort(
        id=workplace.id,
        name=(await get_ask_translation_or_first(workplace.texts, language_code)).name,
        description=(await get_ask_translation_or_first(workplace.texts, language_code)).description,
        languages=[text.language.code for text in workplace.texts]
    ) for workplace in pagination.items]
    return pagination


@router.get("/{workplace_id}", response_model=WorkplaceOut)
async def get_workplace(workplace_id: int, language_code: str = None):
    """ Get a workplace by id """
    if not language_code:
        workplace_text = await WorkPlaceText.filter(workplace_id=workplace_id).prefetch_related("language",
                                                                                                "workplace",
                                                                                                "workplace__instances").order_by("id").first()
    else:
        workplace_text = await WorkPlaceText.get_or_none(workplace_id=workplace_id,
                                                         language__code=language_code).prefetch_related("language",
                                                                                                        "workplace",
                                                                                                        "workplace__instances")
    if workplace_text is None:
        raise HTTPException(status_code=404, detail="Workplace not found in this language")
    return WorkplaceOut(
        id=workplace_text.workplace.id,
        name=workplace_text.name,
        description=workplace_text.description,
        language=workplace_text.language.code,
        anchor=Anchor(
            position=Position(
                x=workplace_text.workplace.x,
                y=workplace_text.workplace.y,
                z=workplace_text.workplace.z
            ),
            rotation=Position(
                x=workplace_text.workplace.u,
                y=workplace_text.workplace.v,
                z=workplace_text.workplace.w
            )
        ) if workplace_text.workplace.x is not None else None,
        artifacts=[ArtifactInstanceOut(
            id=instance.id,
            artifactID=instance.artifact_id,
            position=Position(
                x=instance.x,
                y=instance.y,
                z=instance.z,
            ),
            rotation=Position(
                x=instance.u,
                y=instance.v,
                z=instance.w,
            ),
        ) for instance in workplace_text.workplace.instances],
    )


@router.get("/{workplace_id}/languages", response_model=list[str])
async def get_workplace_languages(workplace_id: int):
    """ Get the available languages for a workplace"""
    return [text.language.code for text in await WorkPlaceText.filter(workplace_id=workplace_id).prefetch_related("language")]


@router.post("/", response_model=IDResponse)
async def create_workplace(workplace: WorkplaceIn, _=Depends(insctructor_required)):
    """ Create a workplace """
    if workplace.anchor is None:
        workplace_db = await WorkPlace.create()
    else:
        workplace_db = await WorkPlace.create(
            x=workplace.anchor.position.x,
            y=workplace.anchor.position.y,
            z=workplace.anchor.position.z,
            u=workplace.anchor.rotation.x,
            v=workplace.anchor.rotation.y,
            w=workplace.anchor.rotation.z,
        )
    await WorkPlaceText.create(
        workplace=workplace_db,
        name=workplace.name,
        description=workplace.description,
        language=await Language.get(code=workplace.language)
    )
    artifacts_instances = []
    for artifact in workplace.artifacts:
        artifacts_instances.append(
            ArtifactInstance(
                workplace=workplace_db,
                artifact_id=artifact.artifactID,
                x=artifact.position.x,
                y=artifact.position.y,
                z=artifact.position.z,
                u=artifact.rotation.x,
                v=artifact.rotation.y,
                w=artifact.rotation.z,
            )
        )
    await ArtifactInstance.bulk_create(artifacts_instances)

    return IDResponse(id=workplace_db.id)


@router.patch("/{workplace_id}")
async def update_workplace(workplace_id: int, workplace: WorkplaceInPatch, language_code: str = None, _=Depends(insctructor_required)):
    """ update a workplace by id """
    workplace_db = await WorkPlace.get(id=workplace_id).prefetch_related("texts__language")
    if not language_code:
        language_code = workplace_db.texts[0].language.code
    workplace_text, created = await WorkPlaceText.get_or_create(workplace_id=workplace_id,
                                                                language_id=(await Language.get(code=language_code)).id,
                                                                defaults={"name": "", "description": ""})
    if created and (workplace_text.name is None or workplace_text.description is None):
        raise HTTPException(status_code=400, detail="You must specify a name and a description for the activity when adding a new language")
    if "name" in workplace.__fields_set__:
        workplace_text.name = workplace.name
    if "description" in workplace.__fields_set__:
        workplace_text.description = workplace.description
    if "anchor" in workplace.__fields_set__:
        if workplace.anchor is None:
            workplace_db.x = None
            workplace_db.y = None
            workplace_db.z = None
            workplace_db.u = None
            workplace_db.v = None
            workplace_db.w = None
        else:
            workplace_db.x = workplace.anchor.position.x
            workplace_db.y = workplace.anchor.position.y
            workplace_db.z = workplace.anchor.position.z
            workplace_db.u = workplace.anchor.rotation.x
            workplace_db.v = workplace.anchor.rotation.y
            workplace_db.w = workplace.anchor.rotation.z
    await workplace_db.save()
    await workplace_text.save()
    return await get_workplace(workplace_id, language_code)


@router.delete("/{workplace_id}")
@atomic()
async def delete_workplace(workplace_id, _=Depends(insctructor_required)):
    """ delete a workplace by id """
    # objects that reference this object are also deleted ( cascade )
    if await WorkPlace.get(id=workplace_id).delete():
        return OKResponse(ok="Workplace deleted")
    else:
        raise HTTPException(status_code=404, detail="Workplace not found")


@router.post("/{workplace_id}/instances", response_model=IDResponse)
async def create_artifact_instance_in_workplace(workplace_id: int, instance: ArtifactInstanceIn, _=Depends(insctructor_required)):
    """ Add an artifact to a workplace """
    instance_db = await ArtifactInstance.create(
        workplace=await WorkPlace.get(id=workplace_id),
        artifact_id=instance.artifactID,
        x=instance.position.x,
        y=instance.position.y,
        z=instance.position.z,
        u=instance.rotation.x,
        v=instance.rotation.y,
        w=instance.rotation.z,
    )
    return IDResponse(id=instance_db.id)


@router.patch("/instances/{instance_id}")
async def update_artifact_instance_in_workplace(instance_id: int, instance: ArtifactInstanceInPatch, _=Depends(insctructor_required)):
    """ update an artifact instance in a workplace by id """
    instance_db = await ArtifactInstance.get(id=instance_id)
    if "artifactID" in instance.__fields_set__:
        instance_db.artifact_id = instance.artifactID
    if "position" in instance.__fields_set__:
        instance_db.x = instance.position.x
        instance_db.y = instance.position.y
        instance_db.z = instance.position.z
    if "rotation" in instance.__fields_set__:
        instance_db.u = instance.rotation.x
        instance_db.v = instance.rotation.y
        instance_db.w = instance.rotation.z
    await instance_db.save()
    return ArtifactInstanceOut(
        id=instance_db.id,
        artifactID=instance_db.artifact_id,
        position=Position(
            x=instance_db.x,
            y=instance_db.y,
            z=instance_db.z,
        ),
        rotation=Position(
            x=instance_db.u,
            y=instance_db.v,
            z=instance_db.w,
        ),
    )


@router.delete("/instances/{instance_id}")
async def delete_artifact_instance_in_workplace(instance_id: int, _=Depends(insctructor_required)):
    """ delete an artifact instance in a workplace by id """
    if await ArtifactInstance.get(id=instance_id).delete():
        return OKResponse(ok="Artifact instance deleted")
    else:
        raise HTTPException(status_code=404, detail="Artifact instance not found")
