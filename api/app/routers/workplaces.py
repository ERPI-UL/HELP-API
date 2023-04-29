from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi_pagination import Page
from fastapi_pagination.ext.tortoise import paginate

from app.models.language import Language
from app.models.workplace import ArtifactInstance, ArtifactInstanceIn, Position, WorkPlace, WorkplaceIn, WorkPlaceText, WorkplaceOut, WorkplaceOutShort
from app.routers.activities import get_ask_translation_or_first
from app.types.response import IDResponse
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
        language=[text.language.code for text in workplace.texts]
    ) for workplace in pagination.items]
    return pagination


@router.get("/{workplace_id}", response_model=WorkplaceOut)
async def get_workplace(workplace_id: int, language_code: str = "fr"):
    """ Get a workplace by id """
    workplace_text = await WorkPlaceText.get(workplace_id=workplace_id, language__code=language_code).prefetch_related("language", "workplace__instances")
    return WorkplaceOut(
        id=workplace_text.workplace.id,
        name=workplace_text.name,
        description=workplace_text.description,
        language=workplace_text.language.code,
        artifacts=[ArtifactInstanceIn(
            id=instance.artifact_id,
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


@router.post("/", response_model=IDResponse)
async def create_workplace(workplace: WorkplaceIn, _=Depends(insctructor_required)):
    """ Create a workplace """
    workplace_db = await WorkPlace.create()
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
                artifact_id=artifact.id,
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
