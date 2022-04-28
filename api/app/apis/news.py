#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
API for news
"""

from typing import List, Any

from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from starlette.responses import Response

from models.user import User as UserDAO, verify_user_password
from schemas.user import UserOut, UserIn, UserUpdate, PasswordChange
from tools.auth import get_current_user
from tools.crypto import generate_salt, hash_password
from tools.db import get_db

router = APIRouter(
    prefix="/news",
    tags=["news"],
)


@router.get('/', response_model=List[UserOut], dependencies=[Depends(get_db)])
def list_user() -> List[UserOut]:
    """
    List all user
    """
    return list(UserDAO.select())


class News(BaseModel):
    """News object"""
    name: str = Field(..., description='News name', example='Why the Answer to the Ultimate Question of Life,'
                                                            + 'The Universe, and Everything is 42 ?')
    campaign: int = Field(..., description='Campaign which the news is about', example=0)

    class Config:
        orm_mode = True


class NewsOut(News):
    id: Optional[int] = Field(None, description='News identifier')
    author: int = Field(..., description='Author who wrote the article', example=0)
    created_at: int = Field(..., description='When the news was created', example=datetime.datetime.utcnow)
    updated_at: int = Field(..., description='When the news was edited', example=datetime.datetime.utcnow)


class NewsUpdate(News, metaclass=AllOptional):
    pass


class NewContent(BaseModel):
    """News content schema
    The content is moved to another schema to avoid transferring too much data when asking the news
    """
    content: Optional[str] = Field(None, description='Contant of the news',
                                   example='Lorem ipsum dolor sit amet, consectetur adipiscing elit. In euismod feli'
                                           + 'eget nulla porta, sed condimentum magna hendrerit.')
