from passlib.hash import bcrypt
from pydantic import BaseModel
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


class UserinPut(BaseModel):
    """ Model to send User to the API"""
    username: str
    firstname: str
    lastname: str
    email: str
    languageCode: str


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
