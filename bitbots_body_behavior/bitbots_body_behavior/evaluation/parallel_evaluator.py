from typing import Iterable

from bitbots_body_behavior.execution import ProcessPoolExecutor

from . import ActionEvaluator, Evaluation, EvaluationResult, Evaluator


class ParallelEvaluator(Evaluator):
    def __init__(self, max_workers: int = 4) -> None:
        self.executor = ProcessPoolExecutor(max_workers)

    def evaluate_actions(self, evaluations: Iterable[Evaluation]) -> list[EvaluationResult]:
        return self.executor.map(ActionEvaluator.evaluate, evaluations)
