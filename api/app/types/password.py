from pydantic import BaseModel


class PasswordChange(BaseModel):
    """ PasswordChange pydantic model"""
    username: str
    old: str
    new: str


class PasswordReset(BaseModel):
    """ PasswordReset pydantic model"""
    token: str
    password: str
