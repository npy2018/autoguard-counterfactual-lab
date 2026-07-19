from autoguard_cf.demo import run
from autoguard_cf.planner import BayesianExperimentPlanner
from autoguard_cf.schemas import Experiment, Hypothesis


def test_demo_prefers_high_value_parameter_experiment() -> None:
    result = run()
    assert result["chosen_experiment"]["intervention_type"] == "parameter"
    assert result["result"]["anomaly_removed"] is True
    assert result["result"]["posterior"]["H1"] > 0.8


def test_planner_downweights_low_reliability_pixel_test() -> None:
    hypotheses = [Hypothesis(hypothesis_id="H1", statement="a", prior=0.5), Hypothesis(hypothesis_id="H2", statement="b", prior=0.5)]
    experiments = [
        Experiment(experiment_id="A", name="parameter", intervention_type="parameter", target="x", value="1", reliability="A", likelihood_positive={"H1": 0.9, "H2": 0.1}),
        Experiment(experiment_id="D", name="pixels", intervention_type="environment", target="image", value="edit", reliability="D", likelihood_positive={"H1": 0.99, "H2": 0.01}),
    ]
    assert BayesianExperimentPlanner().choose(hypotheses, experiments).experiment_id == "A"
