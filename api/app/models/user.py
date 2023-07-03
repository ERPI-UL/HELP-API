from pydantic import EmailStr
from typing import Optional

from passlib.hash import bcrypt
from pydantic import BaseModel, StrictStr, validator
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


class User(Model):
    """User model"""
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128)
    firstname = fields.TextField()
    lastname = fields.TextField()
    email = fields.CharField(128, unique=True)
    adminLevel = fields.IntField(default=0)
    language = fields.ForeignKeyField(
        "models.Language", related_name="users", null=True)

    def verify_password(self, password):
        """Verify a password against the stored hash"""
        return bcrypt.verify(password, self.password_hash)

    @staticmethod
    def encrypt_password(password):
        """Encrypt a password using bcrypt"""
        return bcrypt.hash(password)

    class Meta:
        """Meta class for User model"""
        table = "users"


class UserCreate(BaseModel):
    """ Model to create User in the API"""
    username: str
    firstname: str
    lastname: str
    email: str
    password: str
    languageCode: str | None = None

    @validator('languageCode')
    @classmethod
    def language_code_iso_639_1(cls, value):
        """ Validator for languageCode """
        if value:
            if len(value) != 2:
                raise ValueError("LanguageCode must be ISO 639-1")
        return value


class UserInPatch(BaseModel):
    """ Model to send User to the API"""
    username: Optional[StrictStr]
    firstname: Optional[StrictStr]
    lastname: Optional[StrictStr]
    email: Optional[EmailStr]
    language_code: Optional[StrictStr]

    @validator('username')
    @classmethod
    def username_must_not_be_empty(cls, value):
        """ Validator for username """
        if not value.strip():
            raise ValueError("Username value must not be empty or null")
        return value

    @validator('firstname')
    @classmethod
    def firstname_must_not_be_empty(cls, value):
        """ Validator for firstname """
        if not value.strip():
            raise ValueError("Firstname value must not be empty or null")
        return value

    @validator('lastname')
    @classmethod
    def lastname_must_not_be_empty(cls, value):
        """ Validator for lastname """
        if not value.strip():
            raise ValueError("Lastname value must not be empty or null")
        return value

    @validator('email')
    @classmethod
    def email_must_not_be_empty(cls, value):
        """ Validator for email """
        if not value.strip():
            raise ValueError("Email value must not be empty or null")
        return value

    @validator('language_code')
    @classmethod
    def language_code_must_not_be_empty(cls, value):
        """ Validator for languageCode """
        if not value.strip():
            raise ValueError("LanguageCode value must not be empty or null")
        return value


class ShortUserOut(BaseModel):
    """ Model to send User to the API"""
    id: int
    username: str
    firstname: str
    lastname: str

    class Config:
        """ Config class for ShortUserOut"""
        orm_mode = True


User_Pydantic = pydantic_model_creator(User, name='User')
UserIn_Pydantic = pydantic_model_creator(
    User, name='UserIn', exclude_readonly=True)
UserNew = pydantic_model_creator(
    User, name='UserNew', exclude_readonly=True, exclude=['adminLevel'])
# User à envoyer au front sans le mot de passe
UserinFront = pydantic_model_creator(
    User, name='UserinFront', exclude=['password_hash'])
UserinToken = pydantic_model_creator(User, name='UserinToken', exclude=[
                                     'password_hash', 'email', 'firstname', 'lastname'])
