import aiofiles
from aioshutil import rmtree
from fastapi import Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.routing import APIRouter
from fastapi_pagination import Page
from fastapi_pagination.ext.tortoise import paginate
from tortoise.transactions import atomic

from app.models.artifact import (Artifact, ArtifactIn, ArtifactInPatch,
                                 ArtifactOut, ArtifactOutShort, ArtifactText)
from app.models.language import Language
from app.routers.activities import get_ask_translation_or_first
from app.types.response import IDResponse, OKResponse
from app.utils import MODELS_DIRECTORY, insctructor_required

router = APIRouter()


@router.get("/", response_model=Page)
async def get_artifacts(language_code: str = 'fr'):
    """ Get all artifacts """
    pagination = await paginate(Artifact.all().prefetch_related("texts", "texts__language", "targets").order_by("id"))
    pagination.items = [ArtifactOutShort(
        id=artifact.id,
        name=(await get_ask_translation_or_first(artifact.texts, language_code)).name,
        description=(await get_ask_translation_or_first(artifact.texts, language_code)).description,
        language=[text.language.code for text in artifact.texts]
    ) for artifact in pagination.items]
    return pagination


@router.get("/{artifact_id}")
async def get_artifact(artifact_id: int, language_code: str = 'fr'):
    """ Get an artifact"""
    artifact_text = await ArtifactText.get(artifact_id=artifact_id, language__code=language_code).prefetch_related("language", "artifact__targets")
    return ArtifactOut(
        id=artifact_text.artifact.id,
        name=artifact_text.name,
        description=artifact_text.description,
        language=artifact_text.language.code,
        targets=[target.id for target in artifact_text.artifact.targets],
    )


@router.patch("/{artifact_id}", response_model=ArtifactOut)
@atomic()
async def patch_artifact(artifact_id: int, artifact: ArtifactInPatch, language_code: str, _=Depends(insctructor_required)):
    """ Patch an artifact """
    artifact_text, created = await ArtifactText.get_or_create(artifact_id=artifact_id,
                                                              language_id=(await Language.get(code=language_code)).id,
                                                              defaults={"name": "", "description": ""})
    if created and (artifact.name is None or artifact.description is None):
        raise HTTPException(status_code=400, detail="You must specify a name and a description for the artifact when adding a new language")
    if "name" in artifact.__fields_set__:
        artifact_text.name = artifact.name
    if "description" in artifact.__fields_set__:
        artifact_text.description = artifact.description
    await artifact_text.save()
    return await get_artifact(artifact_id, language_code)


@router.post("/")
@atomic()
async def create_artifact(artifact: ArtifactIn, _=Depends(insctructor_required)):
    """ Create an artifact """
    artifact_db = await Artifact.create()
    await ArtifactText.create(
        name=artifact.name,
        description=artifact.description,
        language=await Language.get(code=artifact.language),
        artifact=artifact_db
    )
    return IDResponse(id=artifact_db.id)


@router.delete("/{artifact_id}")
@atomic()
async def delete_artifact(artifact_id: int, _=Depends(insctructor_required)):
    """ Delete an artifact """
    await Artifact.get(id=artifact_id).delete()
    # delete directory with models
    await rmtree(f"{MODELS_DIRECTORY}{artifact_id}")
    return IDResponse(id=artifact_id)


@router.get("/{artifact_id}/model", response_class=FileResponse)
async def get_artifact_model(artifact_id: int):
    """ Get the model of an artifact """
    try:
        await aiofiles.os.stat(f"{MODELS_DIRECTORY}{artifact_id}/artifact.glb")
        return FileResponse(f"{MODELS_DIRECTORY}{artifact_id}/artifact.glb", media_type="application/octet-stream", filename="artifact.glb")
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Model not found") from exc


@router.put("/{artifact_id}/model")
@atomic()
async def update_artifact_model(artifact_id: int, model: UploadFile, _=Depends(insctructor_required)):
    """ Update the model of an artifact """
    path = f"{MODELS_DIRECTORY}{artifact_id}"
    # create directory if not exist
    await aiofiles.os.makedirs(path, exist_ok=True)
    content = await model.read()
    # size does not exceed 2 Mio
    if len(content) > 2 * 1024 * 1024:
        raise ValueError("File size is too large")
    # write file
    async with aiofiles.open(f"{path}/artifact.glb", "wb") as file:
        await file.write(content)
    return OKResponse(ok="Model updated")
