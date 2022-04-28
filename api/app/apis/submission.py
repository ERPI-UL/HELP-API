#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
API of User management
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
    prefix="/user",
    tags=["user"],
)


class Submission(BaseModel):
    """Submission schema"""
    node: int = Field(..., description='Node to which the data was submitted', example=0)
    submitter: int = Field(..., description='User who submitted the data', example=0)
    data: Json = Field(..., description='The submitted data', example={})
    is_complete: bool = Field(..., description='If the data is final', example=True)

    class Config:
        orm_mode = True


class SubmissionOut(Submission):
    id: Optional[int] = Field(None, description='Campaign Node identifier')
    created_at: int = Field(..., description='When the submission was created', example=datetime.datetime.utcnow)
    updated_at: int = Field(..., description='When the submission was edited', example=datetime.datetime.utcnow)


class SubmissionUpdate(Submission, metaclass=AllOptional):
    pass
