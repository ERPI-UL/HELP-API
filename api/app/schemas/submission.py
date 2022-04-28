#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Definition of submission schema
"""
from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel, Field, Json
import peewee as pw
from pydantic.utils import GetterDict

from schemas import AllOptional


class SubmissionGetter(GetterDict):
    def get(self, key: Any, default: Any = None) -> Any:
        if key == 'node':
            return self._obj.node.id
        if key == 'submitter':
            return self._obj.submitter.id
        res = getattr(self._obj, key, default)
        if isinstance(res, pw.ModelSelect):
            return list(res)
        return res


class Submission(BaseModel):
    """Submission schema"""
    node: int = Field(..., description='Node to which the data was submitted', example=0)
    submitter: int = Field(..., description='User who submitted the data', example=0)
    data: Json = Field(..., description='The submitted data', example={})
    is_complete: bool = Field(..., description='If the data is final', example=True)

    class Config:
        orm_mode = True
        getter_dict = SubmissionGetter


class SubmissionOut(Submission):
    id: Optional[int] = Field(None, description='Campaign Node identifier')
    created_at: Optional[datetime] = Field(..., description='When the submission was created', example=datetime.utcnow())
    updated_at: Optional[datetime] = Field(..., description='When the submission was edited', example=datetime.utcnow())


class SubmissionUpdate(Submission, metaclass=AllOptional):
    pass
