from __future__ import annotations

from copy import deepcopy

from .schemas import Experiment, ReplayFrame


def run_intervention(frames: list[ReplayFrame], experiment: Experiment) -> list[ReplayFrame]:
    result = deepcopy(frames)
    if experiment.intervention_type == "parameter" and experiment.target == "pedestrian_threshold":
        threshold = float(experiment.value)
        for frame in result:
            if frame.pedestrian_confidence < threshold:
                frame.object_class = "static_unknown"
                frame.planner_risk = min(frame.planner_risk, 0.25)
                frame.acceleration_command_mps2 = max(frame.acceleration_command_mps2, -0.3)
    elif experiment.intervention_type == "module" and experiment.target == "perception_model":
        for frame in result:
            frame.object_class = "static_unknown"
            frame.planner_risk *= 0.35
            frame.acceleration_command_mps2 = max(frame.acceleration_command_mps2, -0.35)
    elif experiment.intervention_type == "object" and experiment.target == "object_328.class":
        for frame in result:
            frame.object_class = experiment.value
            frame.planner_risk *= 0.3
            frame.acceleration_command_mps2 = max(frame.acceleration_command_mps2, -0.25)
    elif experiment.intervention_type == "environment":
        # Environment/pixel interventions are intentionally not treated as validated replay.
        return result
    return result


def anomaly_removed(frames: list[ReplayFrame], threshold: float = -1.5) -> bool:
    return min(frame.acceleration_command_mps2 for frame in frames) > threshold
