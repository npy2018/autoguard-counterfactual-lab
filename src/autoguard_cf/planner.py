from __future__ import annotations

import math

from .schemas import Experiment, Hypothesis


def entropy(probabilities: list[float]) -> float:
    return -sum(p * math.log(p + 1e-12) for p in probabilities)


def normalize(values: dict[str, float]) -> dict[str, float]:
    total = sum(values.values())
    return {key: value / total for key, value in values.items()}


class BayesianExperimentPlanner:
    def choose(self, hypotheses: list[Hypothesis], experiments: list[Experiment]) -> Experiment:
        prior = normalize({item.hypothesis_id: item.prior for item in hypotheses})
        current_entropy = entropy(list(prior.values()))
        best = None
        best_gain = -1.0
        for experiment in experiments:
            p_positive = sum(prior[h] * experiment.likelihood_positive[h] for h in prior)
            positive = normalize({h: prior[h] * experiment.likelihood_positive[h] for h in prior})
            negative = normalize({h: prior[h] * (1 - experiment.likelihood_positive[h]) for h in prior})
            expected = p_positive * entropy(list(positive.values())) + (1 - p_positive) * entropy(list(negative.values()))
            reliability_weight = {"A": 1.0, "B": 0.85, "C": 0.6, "D": 0.25}[experiment.reliability]
            gain = (current_entropy - expected) * reliability_weight
            if gain > best_gain:
                best = experiment
                best_gain = gain
        if best is None:
            raise ValueError("no experiments")
        return best

    def update(self, hypotheses: list[Hypothesis], experiment: Experiment, positive: bool) -> dict[str, float]:
        weights = {}
        for hypothesis in hypotheses:
            likelihood = experiment.likelihood_positive[hypothesis.hypothesis_id]
            weights[hypothesis.hypothesis_id] = hypothesis.prior * (likelihood if positive else 1 - likelihood)
        return normalize(weights)
