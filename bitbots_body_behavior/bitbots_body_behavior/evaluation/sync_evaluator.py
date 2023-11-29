from typing import Iterable

from . import ActionEvaluator, Evaluation, EvaluationResult


class SyncEvaluator:
    def evaluate_actions(self, evaluations: Iterable[Evaluation]) -> list[EvaluationResult]:
        return map(ActionEvaluator.evaluate, list(evaluations))
