from fastapi.routing import APIRouter
from fastapi_pagination import Page
from fastapi_pagination.ext.tortoise import paginate
from tortoise.transactions import atomic

from app.models.artifact import (Artifact, ArtifactIn, ArtifactOut,
                                 ArtifactOutShort, ArtifactText)
from app.models.language import Language
from app.routers.activities import get_ask_translation_or_first
from app.types.response import IDResponse

router = APIRouter()


@router.get("/", response_model=Page)
async def get_artifacts(language_code: str = 'fr'):
    """ Get all artifacts """
    pagination = await paginate(Artifact.all().prefetch_related("texts", "texts__language", "targets").order_by("id"))
    pagination.items = [ArtifactOutShort(
        id=artifact.id,
        name=(await get_ask_translation_or_first(artifact.texts, language_code)).name,
        description=(await get_ask_translation_or_first(artifact.texts, language_code)).description,
        language=[text.language.code for text in artifact.texts],
        targets=[target.id for target in artifact.targets],
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


@router.post("/")
@atomic()
async def create_artifact(artifact: ArtifactIn):
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
async def delete_artifact(artifact_id: int):
    """ Delete an artifact """
    await Artifact.get(id=artifact_id).delete()
    return IDResponse(id=artifact_id)
