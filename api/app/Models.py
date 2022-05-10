# from sqlalchemy.orm import declarative_base
# from sqlalchemy import Column, Integer, String
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:root@localhost/indico"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()


# engine.connect()


# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     username = Column(String(50), unique=True)
#     password_hash = Column(String(60))
#     fullname = Column(String(200))
#     email = Column(String(254))
#     adminLevel = Column(Integer, default=0)

#     class Config:
#         orm_mode = True

#     def __repr__(self):
#         return "<User(name='%s', fullname='%s', nickname='%s')>" % (self.name, self.fullname, self.nickname)

# Base.metadata.create_all(bind=engine)

# user = User(username='test', password_hash='test')

# # save user
# session = SessionLocal()
# session.add(user)
# session.commit()
from secrets import choice
from requests import session
from tortoise import OneToOneFieldInstance, Tortoise, fields, run_async
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from tortoise.models import Model
from passlib.hash import bcrypt
from pydantic import BaseModel, validate_arguments

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
    scenarios: fields.ReverseRelation["Scenario"]
    targets = fields.ManyToManyField('models.Target', related_name='machine')

    class Meta:
        table = "machines"


class Scenario(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    description = fields.TextField(null=True)
    machine: fields.ForeignKeyField(
        model_name="models.Machine", related_name="scenarios")

    class Meta:
        table = "scenarios"
        # unique_together = ('name', 'scenarios.machineName')


class Step(Model):
    id = fields.IntField(pk=True)
    label = fields.TextField()
    type = fields.ForeignKeyField('models.Type', related_name='steps')
    name = fields.TextField()
    description = fields.TextField()
    scenario = fields.ForeignKeyField('models.Scenario', related_name='steps')

    class Meta:
        table = "steps"


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

    class Meta:
        table = "steps_target"


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


class Session(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        'models.User', related_name='sessions')
    scenario = fields.ForeignKeyField(
        'models.Scenario', related_name='sessions')
    date = fields.DatetimeField(auto_now_add=True)
# class UserinFront(BaseModel):
#     id: int
#     username: str
#     adminLevel: int


class Easy(BaseModel):
    code: int
    token: str


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
# type = Type(name="test")
# type.save()
# step = Step(label="test",type=type,name="test",description="test")
# step.save()
# scenario = Scenario(name="test",description="test",steps=[step,step])
# scenario.save()


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
    name: str


class StepPost(BaseModel):
    name: str
    title: str
    description: str
    type: str
    targets: list[str]
    choices: list[str] = None


class ChoicePost(BaseModel):
    option_left: str


class ScenarioPost(BaseModel):
    title: str
    machine: MachinePost
    steps: list[StepPost]


class playedStepPost(BaseModel):
    progressNumber: int
    missed: bool
    skipped: bool
    record: str
    stepid: int
    sessionid: int


class SessionIn(BaseModel):
    userid: int
    scenarioid: int
    date: str


class PasswordChange(BaseModel):
    username: str
    old: str
    new: str

    # playedSteps:list[playedStepIn]
SessioninFront = pydantic_model_creator(
    Session, name='SessioninFront', exclude_readonly=True)
playedStepIn = pydantic_model_creator(
    playedStep, name='playedStepIn')
