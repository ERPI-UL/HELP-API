#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
API of campaign management
"""

from datetime import datetime
from typing import List, Any

from fastapi import APIRouter, HTTPException, Depends
from peewee import JOIN
from playhouse.shortcuts import model_to_dict
from starlette import status
from starlette.responses import Response

from apis.user import user_not_found
from models.campaign import Campaign as CampaignDAO, get_campaign_if_available, get_campaign_if_editable
from models.campaign_perm import CampaignPermission as CampaignPermissionDAO, CampaignPermission
from models.user import User as UserDAO
from schemas.campaign import Campaign, CampaignOut, CampaignUpdate
from schemas.campaign_perm import CampaignPermission, CampaignPermissionIn
from tools.auth import get_current_user
from tools.db import get_db

router = APIRouter(
    prefix="/campaign",
    tags=["campaign"],
)

campaign_not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="This campaign doesn't exist or you don't have the rights to see it.")


@router.get('/', response_model=List[CampaignOut], dependencies=[Depends(get_db)])
def list_campaign(login_info: tuple[UserDAO, List[str]] = Depends(get_current_user)) -> List[CampaignOut]:
    """
    List campaigns that can be seen by the connected user
    """
    user, _ = login_info
    return list(CampaignDAO.select()
                .join(CampaignPermissionDAO, JOIN.LEFT_OUTER)
                .where(((CampaignPermissionDAO.user == user)
                        | (CampaignPermissionDAO.user.is_null()))
                       & ((CampaignDAO.owner == user)
                          | ((CampaignDAO.is_public == True) & (CampaignPermissionDAO.can_view != False))
                          | ((CampaignDAO.is_public == False) & (CampaignPermissionDAO.can_view == True)))))


@router.post('/', response_model=CampaignOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_db)])
def create_campaign(body: Campaign, login_info: tuple[UserDAO, List[str]] = Depends(get_current_user)) -> CampaignOut:
    """
    Create a new campaign
    """
    user, _ = login_info
    payload = body.dict()

    campaign = CampaignDAO(**payload, owner=user)
    campaign.save()
    return campaign


@router.get('/{campaign_id}', response_model=CampaignOut, dependencies=[Depends(get_db)])
def get_campaign(campaign_id: int, login_info: tuple[UserDAO, List[str]] = Depends(get_current_user)) -> CampaignOut:
    """
    Get a campaign given its identifier
    """
    user, _ = login_info
    campaign = get_campaign_if_available(campaign_id, user)
    if campaign is None:
        raise campaign_not_found
    return campaign


@router.put('/{campaign_id}', response_model=CampaignOut, dependencies=[Depends(get_db)])
def update_campaign(campaign_id: int, body: CampaignUpdate, login_info: tuple[UserDAO, List[str]] = Depends(get_current_user))\
        -> CampaignOut:
    """
    Update a campaign given its identifier
    """
    user, _ = login_info
    payload = body.dict(exclude_unset=True)

    campaign = get_campaign_if_editable(campaign_id, user)
    if campaign is None:
        raise campaign_not_found
    CampaignDAO.update(payload).where(CampaignDAO.id == campaign_id).execute()
    return CampaignDAO[campaign_id]


@router.delete('/{campaign_id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_db)])
def delete_campaign(campaign_id: int, login_info: tuple[UserDAO, List[str]] = Depends(get_current_user)) -> Response:
    """
    Delete a campaign given its identifier
    """
    user, _ = login_info
    campaign = get_campaign_if_editable(campaign_id, user)
    if campaign is None:
        raise campaign_not_found
    campaign.delete_instance()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


"""
Studies Permissions
"""


@router.get('/{campaign_id}/perms', response_model=List[CampaignPermission], dependencies=[Depends(get_db)])
def list_campaign_perm(campaign_id: int, login_info: tuple[UserDAO, List[str]] = Depends(get_current_user))\
        -> List[CampaignPermission]:
    """
    List all perms of a campaign
    """
    user, _ = login_info
    campaign = get_campaign_if_editable(campaign_id, user)
    if campaign is None:
        raise campaign_not_found
    return list(CampaignPermissionDAO.select()
                .where(CampaignPermissionDAO.campaign == campaign))


@router.get('/{campaign_id}/perms/{user_id}', response_model=CampaignPermission, dependencies=[Depends(get_db)])
def get_campaign_perm(campaign_id: int, user_id: int, login_info: tuple[UserDAO, List[str]] = Depends(get_current_user))\
        -> CampaignPermission:
    """
    Get a campaign perm given its campaign and user
    """
    user, _ = login_info
    campaign = get_campaign_if_editable(campaign_id, user)
    if campaign is None:
        raise campaign_not_found
    try:
        user2 = UserDAO.get(UserDAO.id == user_id)
    except UserDAO.DoesNotExist:
        raise user_not_found
    perm = CampaignPermissionDAO.get_or_none((CampaignPermissionDAO.campaign == campaign_id)
                                          & (CampaignPermissionDAO.user == user_id))
    if perm is None:
        return CampaignPermission(
            campaign=campaign_id,
            user=user_id,
            can_view=campaign.can_view(user2),
            can_edit=campaign.can_edit(user2),
            can_view_inherited=True,
            can_edit_inherited=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow())

    perm_out = model_to_dict(perm, recurse=False)
    if perm_out['can_view'] is None:
        perm_out['can_view'] = campaign.can_view(user2)
        perm_out['can_view_inherited'] = True
    if perm_out['can_edit'] is None:
        perm_out['can_edit'] = campaign.can_edit(user2)
        perm_out['can_edit_inherited'] = True
    return CampaignPermission(**perm_out)


@router.put('/{campaign_id}/perms/{user_id}', response_model=CampaignPermission, dependencies=[Depends(get_db)])
def update_campaign_perm(campaign_id: int, user_id: int, body: CampaignPermissionIn,
                      login_info: tuple[UserDAO, List[str]] = Depends(get_current_user))\
        -> CampaignPermission:
    """
    Update a campaign perm given the campaign and user
    """
    user, _ = login_info
    payload = body.dict(exclude_unset=True)

    campaign = get_campaign_if_editable(campaign_id, user)
    if campaign is None:
        raise campaign_not_found
    try:
        user2 = UserDAO.get(UserDAO.id == user_id)
    except UserDAO.DoesNotExist:
        raise user_not_found
    perm = CampaignPermissionDAO.get_or_none((CampaignPermissionDAO.campaign == campaign_id)
                                          & (CampaignPermissionDAO.user == user_id))

    print(payload)
    if perm is None:
        payload['campaign'] = campaign_id
        payload['user'] = user_id
        perm = CampaignPermissionDAO(**payload)
        perm.save(force_insert=True)
        perm_out = model_to_dict(perm, recurse=False)
    else:
        CampaignPermissionDAO.update(payload).where((CampaignPermissionDAO.campaign == campaign_id)
                                                 & (CampaignPermissionDAO.user == user_id)).execute()
        perm_out = model_to_dict(perm, recurse=False)
        perm_out.update(**payload)
        if ('can_view' not in payload or payload['can_view'] is None)\
                and ('can_edit' not in payload or payload['can_edit'] is None):
            perm.delete_instance()

    if perm_out['can_view'] is None:
        perm_out['can_view'] = campaign.can_view(user2)
        perm_out['can_view_inherited'] = True
    if perm_out['can_edit'] is None:
        perm_out['can_edit'] = campaign.can_edit(user2)
        perm_out['can_edit_inherited'] = True
    return CampaignPermission(**perm_out)


@router.delete('/{campaign_id}/perms/{user_id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_db)])
def delete_campaign_perm(campaign_id: int, user_id: int,
                      login_info: tuple[UserDAO, List[str]] = Depends(get_current_user)) -> Response:
    """
    Delete a campaign perl given the campaign and user. Put the perm in inherited state
    """
    user, _ = login_info
    campaign = get_campaign_if_editable(campaign_id, user)
    if campaign is None:
        raise campaign_not_found
    try:
        user2 = UserDAO.get(UserDAO.id == user_id)
    except UserDAO.DoesNotExist:
        raise user_not_found
    perm = CampaignPermissionDAO.get_or_none((CampaignPermissionDAO.campaign == campaign)
                                          & (CampaignPermissionDAO.user == user2))

    if perm is not None:
        perm.delete_instance()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
