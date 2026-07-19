from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ReplayFrame(BaseModel):
    timestamp_s: float
    object_class: str
    pedestrian_confidence: float
    planner_risk: float
    acceleration_command_mps2: float


class Hypothesis(BaseModel):
    hypothesis_id: str
    statement: str
    prior: float = Field(gt=0, lt=1)


class Experiment(BaseModel):
    experiment_id: str
    name: str
    intervention_type: Literal["parameter", "module", "object", "environment"]
    target: str
    value: str
    reliability: Literal["A", "B", "C", "D"]
    likelihood_positive: dict[str, float]


class ExperimentResult(BaseModel):
    experiment_id: str
    anomaly_removed: bool
    baseline_min_acceleration: float
    result_min_acceleration: float
    posterior: dict[str, float]
    evidence_grade: str
    conclusion: str


class FieldTestTask(BaseModel):
    title: str
    controlled_variables: list[str]
    collection_requirements: list[str]
    pass_criteria: list[str]
