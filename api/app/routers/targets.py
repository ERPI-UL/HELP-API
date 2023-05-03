from fastapi.routing import APIRouter

from app.models.target import Target, TargetIn, TargetInUpdate, TargetOut
from app.types.response import IDResponse, OKResponse

router = APIRouter()


@router.get("/{target_id}", response_model=TargetOut)
async def get_target(target_id: int):
    """ Get a target"""
    target_db = await Target.get(id=target_id).prefetch_related("componentInstances")
    return TargetOut(
        id=target_db.id,
        name=target_db.name,
        artifact=target_db.artifact_id,
        components=[component.id for component in target_db.componentInstances]
    )


@router.post("/")
async def create_target(target: TargetIn):
    """ Create a target """
    target = await Target.create(name=target.name, artifact_id=target.artifact)
    return IDResponse(id=target.id)


@router.patch("/{target_id}")
async def patch_target(target_id: int, target: TargetInUpdate):
    """ Patch a target """
    target_db = await Target.get(id=target_id)
    if "name" in target.__fields_set__:
        target_db.name = target.name
    if "artifact" in target.__fields_set__:
        target_db.artifact_id = target.artifact
    await target_db.save()


@router.delete("/{target_id}")
async def delete_target(target_id: int):
    """ Delete a target """
    await Target.get(id=target_id).delete()
    return OKResponse(ok="Target deleted")
