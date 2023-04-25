import typing
from datetime import datetime, timedelta
from random import randint

from passlib.hash import bcrypt
from pydantic import BaseModel, validator
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


class ScenarioText(Model):
    """ ScenarioText model"""
    id = fields.IntField(pk=True)
    name = fields.TextField()
    description = fields.TextField()
    language = fields.ForeignKeyField(
        'models.Language', related_name='scenarioTexts')
    scenario = fields.ForeignKeyField(
        'models.Scenario', related_name='texts', on_delete=fields.CASCADE)

    class Meta:
        """ Meta class for ScenarioText model"""
        table = "scenariotext"


class Language(Model):
    """ Language model"""
    id = fields.IntField(pk=True)
    unicode = fields.CharField(128)  # \uD83C\uDDEB\uD83C\uDDF7 -> 🇫🇷
    name = fields.CharField(42)  # Français English Español
    code = fields.CharField(2)  # ISO 639-1 en fr en de it etc..

    class Meta:
        """ Meta class for Language model"""
        table = "languages"


class MachineText(Model):
    """ MachineText model"""
    id = fields.IntField(pk=True)
    name = fields.TextField()
    description = fields.TextField()
    language = fields.ForeignKeyField(
        'models.Language', related_name='machineTexts')
    machine = fields.ForeignKeyField(
        'models.Machine', related_name='texts', on_delete=fields.CASCADE)

    class Meta:
        """ Meta class for MachineText model"""
        table = "machinetext"


class Machine(Model):
    """ Machine model"""
    id = fields.IntField(pk=True)
    name = fields.CharField(50, unique=True)
    description = fields.TextField()
    path = fields.TextField(null=True)
    # scenarios: fields.ReverseRelation["Scenario"]

    class Meta:
        """ Meta class for Machine model"""
        table = "machines"


class Scenario(Model):
    """ Scenario model"""
    id = fields.IntField(pk=True)
    name = fields.TextField()
    description = fields.TextField(null=True)
    machine = fields.ForeignKeyField(
        'models.Machine', related_name='scenarios', on_delete=fields.CASCADE)

    class Meta:
        """ Meta class for Scenario model"""
        table = "scenarios"
        # unique_together = ('name', 'scenarios.machineName')


class StepText(Model):
    """ StepText model"""
    id = fields.IntField(pk=True)
    label = fields.TextField()
    description = fields.TextField()
    language = fields.ForeignKeyField(
        'models.Language', related_name='stepTexts')
    step = fields.ForeignKeyField(
        'models.Step', related_name='texts', on_delete=fields.CASCADE)

    class Meta:
        """ Meta class for StepText model"""
        table = "steptext"


class Step(Model):
    """ Step model"""
    id = fields.IntField(pk=True)
    label = fields.TextField()
    type = fields.ForeignKeyField('models.Type', related_name='steps')
    name = fields.TextField()  # logical purpose , do not translate
    description = fields.TextField()
    ressourcePath = fields.TextField(null=True)
    hint = fields.TextField(null=True)
    scenario = fields.ForeignKeyField(
        'models.Scenario', related_name='steps', on_delete=fields.CASCADE)
    targets = fields.ManyToManyField(
        'models.Target', related_name='steps', null=True)
    position = fields.ForeignKeyField(
        'models.Position', related_name='steps', null=True, on_delete=fields.CASCADE)
    choice = fields.ForeignKeyField(
        'models.Choice', related_name='steps', null=True, on_delete=fields.RESTRICT)
    ordernumber = fields.IntField()

    class Meta:
        """ Meta class for Step model"""
        table = "steps"
        unique_together = ('scenario_id', 'ordernumber')
        ordering = ['ordernumber']


class Position(Model):
    """ Position model"""
    id = fields.IntField(pk=True)
    x = fields.FloatField()
    y = fields.FloatField()
    z = fields.FloatField()

    class Meta:
        """ Meta class for Position model"""
        table = "positions"


class Type(Model):
    """ Type model"""
    id = fields.IntField(pk=True)
    name = fields.TextField()
    # choice = fields.ForeignKeyField('models.Choice', related_name='choice',null=True)

    class Meta:
        """ Meta class for Type model"""
        table = "types"


class ChoiceText(Model):
    """ ChoiceText model """
    id = fields.IntField(pk=True)
    labelleft = fields.TextField()
    labelright = fields.TextField()
    redirectleft = fields.TextField()
    redirectright = fields.TextField()
    language = fields.ForeignKeyField(
        'models.Language', related_name='choiceTexts')
    choice = fields.ForeignKeyField(
        'models.Choice', related_name='texts', on_delete=fields.CASCADE)

    class Meta:
        """ Meta class for ChoiceText model"""
        table = "choicetext"


class Choice(Model):
    """ Choice model"""
    id = fields.IntField(pk=True)
    labelleft = fields.TextField()
    labelright = fields.TextField()
    redirectleft = fields.TextField()
    redirectright = fields.TextField()

    class Meta:
        """ Meta class for Choice model"""
        table = "choices"


class Target(Model):
    """ Target model"""
    id = fields.IntField(pk=True)
    name = fields.TextField()
    machine = fields.ForeignKeyField('models.Machine', related_name='targets')

    class Meta:
        """ Meta class for Target model"""
        table = "targets"
        unique_together = ('name', 'machine_id')


class PlayedStep(Model):
    """ playedStep model """
    id = fields.IntField(pk=True)
    step = fields.ForeignKeyField(
        'models.Step', related_name='playedSteps', on_delete=fields.CASCADE)
    session = fields.ForeignKeyField(
        'models.Session', related_name='playedSteps', on_delete=fields.CASCADE)
    progressNumber = fields.IntField(default=0)  # garantie l'ordre des steps
    missed = fields.BooleanField(default=False)
    skipped = fields.BooleanField(default=False)
    record = fields.TextField()  # json
    time = fields.IntField(default=0)

    class Meta:
        """ Meta class for playedStep model"""
        table = "playedSteps"
        ordering = ['progressNumber']


class Session(Model):
    """ Session model"""
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        'models.User', related_name='sessions')
    scenario = fields.ForeignKeyField(
        'models.Scenario', related_name='sessions', on_delete=fields.CASCADE)
    evaluation = fields.BooleanField()
    vrmode = fields.BooleanField(null=True)
    date = fields.DatetimeField(auto_now_add=True)
# class UserinFront(BaseModel):
#     id: int
#     username: str
#     adminLevel: int


class Ressource(Model):
    """ Ressource model , represent a file link to an object"""
    id = fields.IntField(pk=True)
    name = fields.TextField()
    path = fields.TextField()
    type = fields.TextField()

    class Meta:
        """ Meta class for Ressource model"""
        table = "ressources"


class Easy(BaseModel):
    """ Easy model"""
    code: str
    token: str

    class Config:
        """ Config class for Easy model"""
        schema_extra = {
            "example": {
                "code": "56328",
                "token": "jwttoken.5aze5ezfezf.jwtoken"
            }
        }


class IncidentLogs(Model):
    """ IncidentLogs model"""
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='logs')
    date = fields.DatetimeField(auto_now_add=True)
    action = fields.TextField()

    class Meta:
        """ Meta class for IncidentLogs model"""
        table = "logs"


class Reset(Model):
    """ Reset model"""
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='reset')
    token = fields.CharField(128)
    expiration = fields.DatetimeField(
        default=datetime.now() + timedelta(days=1))

    class Meta:
        """ Meta class for Reset model"""
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
    User, name='UserinPut', exclude_readonly=True, exclude=['password_hash', 'adminLevel', 'id'])
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
    Session, name='SessionOut', include=['id', 'date', 'evaluation', 'scenario_id', 'vrmode'])


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


class Pagination(BaseModel):
    """ Pagination pydantic model"""
    total: int
    per_page: int
    current_page: int
    last_page: int
    data: list[typing.Any]


class ScenarioCreate(BaseModel):
    """ ScenarioCreate pydantic model"""
    name: str
    description: str
    machine: int


class MachinePost(BaseModel):
    """ MachinePost pydantic model"""
    name: str = None
    id: int = None


class TargetPost(BaseModel):
    """ TargetPost pydantic model"""
    name: str


class PositionPost(BaseModel):
    """ PositionPost pydantic model"""
    x: float
    y: float
    z: float


class TypePost(BaseModel):
    """ TypePost pydantic model"""
    name: str

    @validator('name')
    @classmethod
    def name_validator(cls, value):
        """ verify if the type is valid"""
        if value not in ['choice', 'info', 'action']:
            raise ValueError('Name must be choice, step or action')
        return value


class ChoiceOptions(BaseModel):
    """ ChoiceOptions pydantic model"""
    label: str
    redirect: str


class ChoicePost(BaseModel):
    """ ChoicePost pydantic model"""
    option_left: ChoiceOptions
    option_right: ChoiceOptions


class StepPost(BaseModel):
    """ StepPost pydantic model"""
    name: str
    label: str
    description: str
    ordernumber: int
    position: PositionPost
    type: TypePost
    targets: list[int] = None
    choice: ChoicePost = None

    @validator('ordernumber')
    @classmethod
    def ordernumber_validator(cls, value):
        """ verify if the ordernumber is valid"""
        if value < 0:
            raise ValueError('ordernumber must be >= 0')
        return value


class ScenarioPost(BaseModel):
    """ ScenarioPost pydantic model"""
    name: str
    description: str
    machine: MachinePost
    steps: list[StepPost]


class PlayedStepPost(BaseModel):
    """ playedStepPost pydantic model"""
    progressNumber: int
    missed: bool
    skipped: bool
    record: str
    stepid: int
    time: int


class SessionIn(BaseModel):
    """ SessionIn pydantic model"""
    scenarioid: int
    date: str
    evaluation: bool
    vrmode: bool = None


class PasswordChange(BaseModel):
    """ PasswordChange pydantic model"""
    username: str
    old: str
    new: str


class PasswordReset(BaseModel):
    """ PasswordReset pydantic model"""
    token: str
    password: str
    # playedSteps:list[playedStepIn]


class ScenarioUpdate(BaseModel):
    """ ScenarioUpdate pydantic model"""
    name: str
    description: str
    idMachine: int


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


SessioninFront = pydantic_model_creator(
    Session, name='SessioninFront', exclude_readonly=True)
playedStepIn = pydantic_model_creator(
    PlayedStep, name='playedStepIn')
LanguageOut = pydantic_model_creator(
    Language, name='LanguageFront', exclude_readonly=True)
LanguageOutWithId = pydantic_model_creator(
    Language, name='LanguageFrontWithId')


class IDResponse(BaseModel):
    """ IDResponse pydantic model"""
    id: int

class StepStat(BaseModel):
    """ Pydantic model to send a scenario stats"""
    id: int
    name: str
    value: float


class ScenarioStats(BaseModel):
    """ Pydantic model to send a scenario stats"""
    id: int
    averageTime: float
    averageSuccessRate: float
    numberOfVRSessions: int
    numberOfARSessions: int
    averageTimeByStep: list[StepStat]
    averageSuccessRateByStep: list[StepStat]
