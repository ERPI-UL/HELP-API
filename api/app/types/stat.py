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
