
from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel, Field
from pydantic.utils import GetterDict
import peewee as pw

from schemas import AllOptional


class UserGetter(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, pw.ModelSelect):
            return list(res)
        return res


class UserBase(BaseModel):
    name: str = Field(..., description='User name', example='Sebastien')
    first_name: str = Field(..., description='User first name', example='Da Silva')
    role: str = Field(..., description="User's role identifier", example='admin')
    username: str = Field(
        None, description='Username', example='xXx_monSeigneur54_xXx'
    )
    email: str = Field(
        None, description='e-mail', example='xxmonseigneurxx@telecomnancy.eu'
    )

    class Config:
        orm_mode = True
        getter_dict = UserGetter


class UserOut(UserBase):
    id: Optional[int] = Field(None, description='User identifier')
    last_login: Optional[datetime] = Field(None, description='Date of the last login')


class PasswordChange(BaseModel):
    old_password: str = Field(None, description='Password', example='BouthierUWU')
    password: str = Field(None, description='Password', example='BouthierOwO')


class UserIn(UserBase):
    password: str = Field(None, description='Password', example='BouthierUWU')
    pass


class UserUpdate(UserBase, metaclass=AllOptional):
    pass
