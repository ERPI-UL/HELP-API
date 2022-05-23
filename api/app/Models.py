from datetime import datetime, timedelta
from tortoise import OneToOneFieldInstance, Tortoise, fields, run_async
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from passlib.hash import bcrypt
from pydantic import BaseModel, validator

import typing


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128)
    firstname = fields.TextField()
    lastname = fields.TextField()
    email = fields.CharField(128, unique=True)
    adminLevel = fields.IntField(default=0)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    def encrypt_password(password):
        return bcrypt.hash(password)

    class Meta:
        table = "users"


class Machine(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(50, unique=True)
    description = fields.TextField()
    # scenarios: fields.ReverseRelation["Scenario"]

    class Meta:
        table = "machines"


class Scenario(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    description = fields.TextField(null=True)
    machine = fields.ForeignKeyField(
        'models.Machine', related_name='scenarios', on_delete=fields.CASCADE)

    class Meta:
        table = "scenarios"
        # unique_together = ('name', 'scenarios.machineName')


class Step(Model):
    id = fields.IntField(pk=True)
    label = fields.TextField()
    type = fields.ForeignKeyField('models.Type', related_name='steps')
    name = fields.TextField()
    description = fields.TextField()
    scenario = fields.ForeignKeyField(
        'models.Scenario', related_name='steps', on_delete=fields.CASCADE)
    targets = fields.ManyToManyField(
        'models.Target', related_name='steps', null=True)
    position = fields.ForeignKeyField(
        'models.Position', related_name='steps', null=True, on_delete=fields.CASCADE)
    choice = fields.ForeignKeyField(
        'models.Choice', related_name='steps', null=True, on_delete=fields.CASCADE)
    ordernumber = fields.IntField()

    class Meta:
        table = "steps"
        unique_together = ('scenario_id', 'ordernumber')
        ordering = ['ordernumber']


class Position(Model):
    id = fields.IntField(pk=True)
    x = fields.FloatField()
    y = fields.FloatField()
    z = fields.FloatField()

    class Meta:
        table = "positions"


class Type(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    # choice = fields.ForeignKeyField('models.Choice', related_name='choice',null=True)

    class Meta:
        table = "types"


class Choice(Model):
    id = fields.IntField(pk=True)
    labelleft = fields.TextField()
    labelright = fields.TextField()
    redirectleft = fields.TextField()
    redirectright = fields.TextField()

    class Meta:
        table = "choices"


class Target(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    machine = fields.ForeignKeyField('models.Machine', related_name='targets')

    class Meta:
        table = "targets"
        unique_together = ('name', 'machine_id')


class playedStep(Model):
    id = fields.IntField(pk=True)
    step = fields.ForeignKeyField('models.Step', related_name='playedSteps')
    session = fields.ForeignKeyField(
        'models.Session', related_name='playedSteps')
    progressNumber = fields.IntField(default=0)  # garantie l'ordre des steps
    missed = fields.BooleanField(default=False)
    skipped = fields.BooleanField(default=False)
    record = fields.TextField()  # json
    time = fields.IntField(default=0)

    class Meta:
        table = "playedSteps"
        ordering = ['progressNumber']


class Session(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        'models.User', related_name='sessions')
    scenario = fields.ForeignKeyField(
        'models.Scenario', related_name='sessions')
    evaluation = fields.BooleanField()
    date = fields.DatetimeField(auto_now_add=True)
# class UserinFront(BaseModel):
#     id: int
#     username: str
#     adminLevel: int


class Easy(BaseModel):
    code: str
    token: str

    class Config:
        schema_extra = {
            "example": {
                "code": "56328",
                "token": "jwttoken.5aze5ezfezf.jwtoken"
            }
        }


class IncidentLogs(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='logs')
    date = fields.DatetimeField(auto_now_add=True)
    action = fields.TextField()

    class Meta:
        table = "logs"

class Reset(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='reset')
    token = fields.CharField(128)
    expiration = fields.DatetimeField(default=datetime.now() + timedelta(days=1))

    class Meta:
        table = "reset"

User_Pydantic = pydantic_model_creator(User, name='User')
UserIn_Pydantic = pydantic_model_creator(
    User, name='UserIn', exclude_readonly=True)
UserNew = pydantic_model_creator(
    User, name='UserNew', exclude_readonly=True, exclude=['adminLevel'])
# User à envoyer au front sans le mot de passe
UserinFront = pydantic_model_creator(
    User, name='UserinFront', exclude=['password_hash'])
UserinPut = pydantic_model_creator(
    User, name='UserinPut', exclude_readonly=True, exclude=['password_hash', 'adminLevel', 'id', 'username'])
UserinToken = pydantic_model_creator(User, name='UserinToken', exclude=[
                                     'password_hash', 'email', 'firstname', 'lastname'])
Machinein = pydantic_model_creator(
    Machine, name='Machinein', exclude_readonly=True)
MachineOut = pydantic_model_creator(
    Machine, name='MachineOut')
ScenarioOut = pydantic_model_creator(
    Scenario, name='ScenarioOut')
TargetOut = pydantic_model_creator(
    Target, name='TargetOut', include=['id', 'name'])
SessionOut = pydantic_model_creator(
    Session, name='SessionOut', include=['id', 'date', 'evaluation', 'scenario_id'])


class pagination(BaseModel):
    total: int
    per_page: int
    current_page: int
    last_page: int
    data: list[typing.Any]


class ScenarioCreate(BaseModel):
    name: str
    description: str
    machine: int


class MachinePost(BaseModel):
    name: str = None
    id: int = None


class TargetPost(BaseModel):
    name: str


class PositionPost(BaseModel):
    x: float
    y: float
    z: float


class TypePost(BaseModel):
    name: str

    @validator('name')
    def name_validator(cls, v):
        if v not in ['choice', 'info', 'action']:
            raise ValueError('Name must be choice, step or action')
        return v


class ChoiceOptions(BaseModel):
    label: str
    redirect: str


class ChoicePost(BaseModel):
    option_left: ChoiceOptions
    option_right: ChoiceOptions


class StepPost(BaseModel):
    name: str
    label: str
    description: str
    position: PositionPost
    type: TypePost
    targets: list[int] = None
    choice: ChoicePost = None
    ordernumber: int

    @validator('ordernumber')
    def ordernumber_validator(cls, v):
        if v < 0:
            raise ValueError('ordernumber must be >= 0')
        return v


class ScenarioPost(BaseModel):
    name: str
    description: str
    machine: MachinePost
    steps: list[StepPost]


class playedStepPost(BaseModel):
    progressNumber: int
    missed: bool
    skipped: bool
    record: str
    stepid: int
    time: int


class SessionIn(BaseModel):
    scenarioid: int
    date: str
    evaluation: bool


class PasswordChange(BaseModel):
    username: str
    old: str
    new: str

class PasswordReset(BaseModel):
    token:str
    password:str
    # playedSteps:list[playedStepIn]
SessioninFront = pydantic_model_creator(
    Session, name='SessioninFront', exclude_readonly=True)
playedStepIn = pydantic_model_creator(
    playedStep, name='playedStepIn')
