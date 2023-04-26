from random import randint

from pydantic import BaseModel, validator


class Invite(BaseModel):
    """ Invite pydantic model"""
    email: str
    firstname: str
    lastname: str
    adminLevel: int = None
    username: str = None

    @validator('adminLevel')
    @classmethod
    def adminlvl_validator(cls, value):
        """ verify if the adminLevel is valid """
        if value not in [1, 2]:
            raise ValueError('adminLevel must be 1 or 2')
        return 1

    @validator('username')
    @classmethod
    def username_validator(cls, value, values):
        """ verify if the username is valid """
        if value is None or value == '':
            value = values['firstname'] + '.' + \
                values['lastname'] + str(randint(1, 1000))
        return value
