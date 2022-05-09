from http.client import INTERNAL_SERVER_ERROR
from anyio import Any
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.hash import bcrypt
from tortoise.contrib.pydantic import pydantic_model_creator
from fastapi_pagination import Page, add_pagination, paginate
from typing import List
import Models
import utils
from tortoise import transactions
from pydantic import parse_obj_as, BaseModel


router = APIRouter()


@router.post('/', response_model=Models.UserinFront)
async def create_user(user: Models.UserNew):
    user_obj = Models.User(username=user.username,
                           password_hash=bcrypt.hash(user.password_hash), firstname=user.firstname, lastname=user.lastname, email=user.email,adminLevel=1)
    await user_obj.save()
    return await Models.UserinFront.from_tortoise_orm(user_obj)


# @router.get('/', response_model=List[Models.UserinFront])
# async def get_users():
#     return await Models.User.all().limit(5).get_or_none()

# list all users
@transactions.atomic()
@router.get('/', response_model=Models.pagination)
async def get_users(page: int = 1, per_page: int = 10, res: Any = Depends(utils.InstructorRequired)):
    users_count = await Models.User.all().count()
    if users_count < per_page:
        per_page = users_count
    # check for zero per_page
    if per_page == 0:
        per_page = 1
    users = await Models.User.all().offset((page - 1) * per_page).limit(per_page)
    # on cache les données sensibles pour le front
    front = parse_obj_as(List[Models.UserinFront], users)
    lastPage = users_count // per_page
    if(page > lastPage):
        raise HTTPException(status_code=404, detail="Page not found")
    return {
        'total': users_count,
        'per_page': per_page,
        'current_page': page,
        'last_page': lastPage,
        'data': front
    }


@router.get('/me', response_model=Models.UserinFront)
async def get_user(current_user: Models.User = Depends(utils.get_current_user_in_token)):
    # user = await Models.UserinFront.from_tortoise_orm(Models.User.get(id=current_user.id))
    user = await Models.User.get(id=current_user.id)
    return await Models.UserinFront.from_tortoise_orm(user)


@router.get('/{id}', response_model=Models.UserinFront)
async def read_user(id: int, current_user: Models.User = Depends(utils.get_current_user_in_token)):
    user = await Models.User.get_or_none(id=8)
    if current_user.adminLevel < utils.Permission.INSTRUCTOR.value and current_user.id != id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    user = await Models.User.get(id=id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return await Models.UserinFront.from_tortoise_orm(user)


@router.put('/me', response_model=Models.UserinFront)
async def update_user(user: Models.UserinPut, current_user: Models.User = Depends(utils.get_current_user_in_token)):
    user_obj = await Models.User.get(id=current_user.id)
    if user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if(len(user.firstname) > 0):
        user_obj.firstname = user.firstname
    if(len(user.lastname) > 0):
        user_obj.lastname = user.lastname
    if(len(user.email) > 0):
        user_obj.email = user.email
    await user_obj.save()
    return await Models.UserinFront.from_tortoise_orm(user_obj)
