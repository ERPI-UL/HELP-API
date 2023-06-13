from pydantic import BaseModel


class Easy(BaseModel):
    """ Easy model"""
    code: str
    token: str = None
    password: str


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
