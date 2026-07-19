from __future__ import annotations

import json
from pathlib import Path

from .field_test import generate_field_test
from .planner import BayesianExperimentPlanner
from .replay import anomaly_removed, run_intervention
from .schemas import Experiment, ExperimentResult, Hypothesis, ReplayFrame


def run(output: Path | None = None) -> dict[str, object]:
    frames = [
        ReplayFrame(timestamp_s=12.2, object_class="static_unknown", pedestrian_confidence=0.2, planner_risk=0.1, acceleration_command_mps2=-0.1),
        ReplayFrame(timestamp_s=12.34, object_class="pedestrian", pedestrian_confidence=0.37, planner_risk=0.8, acceleration_command_mps2=-1.2),
        ReplayFrame(timestamp_s=12.58, object_class="pedestrian", pedestrian_confidence=0.39, planner_risk=0.95, acceleration_command_mps2=-2.4),
    ]
    hypotheses = [
        Hypothesis(hypothesis_id="H1", statement="lower pedestrian threshold", prior=0.6),
        Hypothesis(hypothesis_id="H2", statement="tracker persistence", prior=0.25),
        Hypothesis(hypothesis_id="H3", statement="weather/pixel interaction", prior=0.15),
    ]
    experiments = [
        Experiment(experiment_id="E1", name="restore threshold", intervention_type="parameter", target="pedestrian_threshold", value="0.42", reliability="A", likelihood_positive={"H1": 0.95, "H2": 0.15, "H3": 0.2}),
        Experiment(experiment_id="E2", name="swap perception model", intervention_type="module", target="perception_model", value="V2.6.8", reliability="B", likelihood_positive={"H1": 0.85, "H2": 0.55, "H3": 0.3}),
        Experiment(experiment_id="E3", name="remove billboard pixels", intervention_type="environment", target="front_image", value="no_billboard", reliability="D", likelihood_positive={"H1": 0.6, "H2": 0.1, "H3": 0.8}),
    ]
    planner = BayesianExperimentPlanner()
    chosen = planner.choose(hypotheses, experiments)
    replayed = run_intervention(frames, chosen)
    removed = anomaly_removed(replayed)
    posterior = planner.update(hypotheses, chosen, removed)
    result = ExperimentResult(
        experiment_id=chosen.experiment_id,
        anomaly_removed=removed,
        baseline_min_acceleration=min(frame.acceleration_command_mps2 for frame in frames),
        result_min_acceleration=min(frame.acceleration_command_mps2 for frame in replayed),
        posterior={key: round(value, 4) for key, value in posterior.items()},
        evidence_grade=chosen.reliability,
        conclusion="parameter-level replay supports H1" if removed else "experiment did not remove anomaly",
    )
    payload = {
        "chosen_experiment": chosen.model_dump(),
        "result": result.model_dump(),
        "field_test_if_needed": generate_field_test("rainy-night billboard", ("V2.6.8", "V2.7.0")).model_dump(),
        "method_boundary": "environment interventions are auxiliary evidence only",
    }
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload
