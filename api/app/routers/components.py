from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from tortoise.transactions import atomic

from app.models.componentinstance import (ComponentInstance,
                                          ComponentInstanceIn,
                                          ComponentInstanceInPatch,
                                          ComponentInstanceOut,
                                          PropertyInstance, PropertyInstanceIn)
from app.types.response import IDResponse, OKResponse
from app.utils import insctructor_required

router = APIRouter()


@router.get("/{component_id}", response_model=ComponentInstanceOut)
async def get_component(component_id: int):
    """ Get a component"""
    component = await ComponentInstance.get(id=component_id).prefetch_related("properties")
    return ComponentInstanceOut(
        id=component.id,
        tag=component.tag,
        script=component.script,
        blocks=component.blocks,
        target=component.target_id,
        properties=[PropertyInstanceIn(
            name=property.name,
            value=property.value,
        ) for property in component.properties]
    )


@router.post("/")
@atomic()
async def create_component(component: ComponentInstanceIn, _=Depends(insctructor_required)):
    """ Create a component """
    component_db = await ComponentInstance.create(tag=component.tag, script=component.script, blocks=component.blocks, target_id=component.target)
    properties_db = [PropertyInstance(name=property.name, value=property.value, componentInstance=component_db) for property in component.properties]
    await PropertyInstance.bulk_create(properties_db)
    return IDResponse(id=component_db.id)


@router.patch("/{component_id}", response_model=ComponentInstanceOut)
@atomic()
async def patch_component(component_id: int, component: ComponentInstanceInPatch, _=Depends(insctructor_required)):
    """ Patch a component """
    component_db = await ComponentInstance.get(id=component_id).prefetch_related("properties")
    if "tag" in component.__fields_set__:
        component_db.tag = component.tag
    if "script" in component.__fields_set__:
        component_db.script = component.script
    if "blocks" in component.__fields_set__:
        component_db.blocks = component.blocks
    if "target" in component.__fields_set__:
        component_db.target_id = component.target
    await component_db.save()
    if "properties" in component.__fields_set__:
        properties_db = [PropertyInstance(name=property.name, value=property.value, componentInstance=component_db)
                         for property in component.properties]
        await PropertyInstance.filter(componentInstance=component_db).delete()
        await PropertyInstance.bulk_create(properties_db)
    return await get_component(component_id)


@router.delete("/{component_id}")
@atomic()
async def delete_component(component_id: int, _=Depends(insctructor_required)):
    """ Delete a component """
    if await ComponentInstance.get(id=component_id).delete():
        return OKResponse(ok="Component deleted")
    else:
        raise HTTPException(status_code=404, detail="Component not found")
