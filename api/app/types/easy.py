from pydantic import BaseModel


class Easy(BaseModel):
    """ Easy model"""
    code: str
    token: str = None
    password: str


class EasyCode(BaseModel):
    """ EasyCode model"""
    code: str
    password: str

    class Config:
        """ Config class for EasyCode model"""
        schema_extra = {
            "example": {
                "code": "56328",
                "password": "e6da2a13bcdd39838e7cd41cf333300e"
            }
        }


class EasyToken(BaseModel):
    """ EasyToken model"""
    token: str

    class Config:
        """ Config class for EasyToken model"""
        schema_extra = {
            "example": {
                "token": "jwttoken.5aze5ezfezf.jwtoken"
            }
        }


class EasyConnect(BaseModel):
    """ EasyConnect model"""
    code: str
    token: str

    class Config:
        """ Config class for EasyConnect model"""
        schema_extra = {
            "example": {
                "code": "56328",
                "token": "jwttoken.5aze5ezfezf.jwtoken"
            }
        }
