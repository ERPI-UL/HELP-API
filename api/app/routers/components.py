from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.routing import APIRouter
from tortoise.transactions import atomic

from app.models.componentinstance import (ComponentInstance,
                                          ComponentInstanceIn,
                                          ComponentInstanceInPatch,
                                          ComponentInstanceOut)
from app.types.response import IDResponse, OKResponse
from app.utils import instructor_required

router = APIRouter()


@router.get("/{component_id}", response_model=ComponentInstanceOut)
async def get_component(component_id: int):
    """ Get a component"""
    component = await ComponentInstance.get(id=component_id)
    return ComponentInstanceOut(
        id=component.id,
        tag=component.tag,
        type=component.type,
        script=component.script,
        blocks=component.blocks,
        target=component.target_id,
        properties=component.properties
    )


@router.post("/")
@atomic()
async def create_component(component: ComponentInstanceIn, _=Depends(instructor_required)):
    """ Create a component """
    component_db = await ComponentInstance.create(tag=component.tag, type=component.type, script=component.script, blocks=component.blocks, target_id=component.target, properties=jsonable_encoder(component.properties))
    return IDResponse(id=component_db.id)


@router.patch("/{component_id}", response_model=ComponentInstanceOut)
@atomic()
async def patch_component(component_id: int, component: ComponentInstanceInPatch, _=Depends(instructor_required)):
    """ Patch a component """
    component_db = await ComponentInstance.get(id=component_id)
    if "tag" in component.__fields_set__:
        component_db.tag = component.tag
    if "type" in component.__fields_set__:
        component_db.type = component.type
    if "script" in component.__fields_set__:
        component_db.script = component.script
    if "blocks" in component.__fields_set__:
        component_db.blocks = component.blocks
    if "target" in component.__fields_set__:
        component_db.target_id = component.target
    if "properties" in component.__fields_set__:
        component_db.properties = jsonable_encoder(component.properties)
    await component_db.save()
    return await get_component(component_id)


@router.delete("/{component_id}")
@atomic()
async def delete_component(component_id: int, _=Depends(instructor_required)):
    """ Delete a component """
    if await ComponentInstance.get(id=component_id).delete():
        return OKResponse(ok="Component deleted")
    else:
        raise HTTPException(status_code=404, detail="Component not found")
