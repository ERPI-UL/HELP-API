import base64
import random
from datetime import datetime, timedelta
from typing import List

import tortoise
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.hash import bcrypt
from pydantic import parse_obj_as
from tortoise import transactions
from tortoise.contrib.pydantic import pydantic_model_creator

from app.mail import send_invite_link
from app.models import (Invite, Language, Pagination, Reset, ScenarioOut,
                        Session, User, UserinFront, UserinPut, UserNew)
from app.utils import (insctructor_required, Permission, get_current_user,
                       get_current_user_in_token, sanitizer)

router = APIRouter()


@router.post('/', response_model=UserinFront)
@transactions.atomic()
async def create_user(user: UserNew):
    """ Create a new user """
    user = sanitizer(user)
    user_obj = User(username=user.username,
                    password_hash=bcrypt.hash(user.password_hash), firstname=user.firstname, lastname=user.lastname, email=user.email, adminLevel=1)
    await user_obj.save()
    return await UserinFront.from_tortoise_orm(user_obj)


@router.get('/', response_model=Pagination)
async def get_users(page: int = 1, per_page: int = 10, _=Depends(insctructor_required)):
    """ Return a paginate list of all users"""
    users_count = await User.all().count()
    if users_count < per_page:
        per_page = users_count
    # check for zero per_page
    if per_page == 0:
        per_page = 1
    users = await User.all().offset((page - 1) * per_page).limit(per_page)
    # on cache les données sensibles pour le front
    front = parse_obj_as(List[UserinFront], users)
    # calculate the number of pages
    last_page = users_count // per_page
    if users_count % per_page != 0:
        last_page += 1
    if page > last_page:
        raise HTTPException(status_code=404, detail="Page not found")
    return {
        'total': users_count,
        'per_page': per_page,
        'current_page': page,
        'last_page': last_page,
        'data': front
    }


@router.get('/languages', response_model=List[pydantic_model_creator(Language)], summary="Retourne toutes les langues disponibles dans l'API")
async def get_languages():
    """ Return all languages """
    return await Language.all()


@router.get('/me')
async def get_me(current_user: User = Depends(get_current_user_in_token)):
    """ Return informations about the connected user via the token """
    user = await User.get(id=current_user.id).prefetch_related('language')
    return {
        'id': user.id,
        'username': user.username,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'email': user.email,
        'adminLevel': user.adminLevel,
        'language': user.language.name if user.language is not None else None,
        'flag': user.language.unicode if user.language is not None else None,
        'language_code': user.language.code if user.language is not None else None,
    }


@router.delete('/me')
@transactions.atomic()
async def delete_user(current_user: User = Depends(get_current_user_in_token)):
    """ Delete the connected user """
    user = await User.get(id=current_user.id)
    await user.delete()
    return {'message': 'Votre compte a été supprimée'}


@router.get('/{id_user}', response_model=UserinFront)
async def get_user(id_user: int, current_user: User = Depends(get_current_user_in_token)):
    """ Return informations about a user """
    if current_user.adminLevel < Permission.INSTRUCTOR.value and current_user.id != id_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    user = await User.get(id=id_user)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return await UserinFront.from_tortoise_orm(user)


@router.get('/{id_user}/scenarios', response_model=List[ScenarioOut])
async def get_user_scenarios(id_user: int, current_user: User = Depends(get_current_user_in_token)):
    """ Return all scenarios played by a user """
    user = await User.get_or_none(id=id_user)
    if current_user.adminLevel < Permission.INSTRUCTOR.value and current_user.id != id_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    sessions = await Session.filter(user=user).prefetch_related('scenario').all()
    scenarios = set()
    for session in sessions:
        scenarios.add(session.scenario)
    return scenarios


@router.put('/me', response_model=UserinFront)
async def update_user(user: UserinPut, current_user: User = Depends(get_current_user_in_token)):
    """ Update the connected user """
    user = sanitizer(user)
    user_obj = await User.get(id=current_user.id)
    if user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if len(user.firstname) > 0:
        user_obj.firstname = user.firstname
    if len(user.lastname) > 0:
        user_obj.lastname = user.lastname
    if len(user.email) > 0:
        user_obj.email = user.email
    if len(user.username) > 0:
        user_obj.username = user.username
    try:
        await user_obj.save()
    except tortoise.exceptions.IntegrityError as err:
        if "username" in str(err):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Ce nom d'utilisateur est déjà utilisé") from err
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Adresse déjà utilisée.") from err
    return await UserinFront.from_tortoise_orm(user_obj)


@router.post("/invite", tags=["auth"])
async def invite_user(invite: Invite, user_in_db=Depends(get_current_user), _=Depends(insctructor_required)):
    """ 
    Invite a new user to the platform by sending an email with a link to create an account,
    the user will be able to choose his password
    """
    async with transactions.in_transaction() as transaction:
        try:
            token = base64.b16encode(random.getrandbits(
                256).to_bytes(32, byteorder='little')).decode('utf-8')
            new_user = User(username=invite.username, email=invite.email, password_hash=User.encrypt_password(
                token), firstname=invite.firstname, lastname=invite.lastname, adminLevel=invite.adminLevel)
            await new_user.save()
            invite_in_db = Reset(user=new_user, token=token,
                                 expiration=datetime.now() + timedelta(days=14))
            await invite_in_db.save()
            if invite.adminLevel == 1:
                role = "apprenti"
            elif invite.adminLevel == 2:
                role = "enseignant"
            await send_invite_link(invite.email, invite.username, token, invite.firstname,
                                   invite.lastname, user_in_db.firstname, user_in_db.lastname, role)
        except tortoise.exceptions.IntegrityError as err:
            await transaction.rollback()
            if "username" in str(err):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Ce nom d'utilisateur est déjà utilisé") from err
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Adresse déjà utilisée.") from err
        except Exception as exc:
            await transaction.rollback()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Erreur lors de l'envoi de l'invitation"
            ) from exc
