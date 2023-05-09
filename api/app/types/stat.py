from datetime import datetime
from pydantic import BaseModel


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


class ActionStat(BaseModel):
    """ Pydantic model to send a scenario stats"""
    id: int
    name: str
    start: datetime
    end: datetime = None
    duration: int
    skipped: bool  # true if the action is skipped
    interactions: int  # number of interactions with a component in a action
    help: int  # number of help request in a action


class SessionStat(BaseModel):
    """ Pydantic model used to return stats about a session"""
    id: int
    activity_id: int
    name: str
    start: datetime
    end: datetime
    duration: int
    abandoned: bool
    skippedRate: float  # percentage of skipped actions , skipped actions / total actions
    actions: list[ActionStat]
