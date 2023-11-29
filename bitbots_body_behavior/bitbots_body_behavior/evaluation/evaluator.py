from typing import Iterable, Tuple, Optional

from bitbots_body_behavior.actions import Action
from bitbots_body_behavior.state.state import State

Evaluation = Tuple[Action, State, list[State]]
EvaluationResult = Tuple[Action, Optional[State], float]


class Evaluator:
    def evaluate_actions(self, evaluations: Iterable[Evaluation]) -> list[EvaluationResult]:
        raise NotImplementedError


class ActionEvaluator(Evaluator):
    @staticmethod
    def evaluate(evaluation: Evaluation) -> EvaluationResult:
        action, current_state, new_states = evaluation
        if len(new_states) == 0:
            return (action, None, action.evaluate(current_state))
        else:
            return max(ActionEvaluator.evaluate_new_states(evaluation), key=lambda item: item[2])

    @staticmethod
    def evaluate_new_states(evaluation: Evaluation) -> Iterable[EvaluationResult]:
        action, current_state, new_states = evaluation

        return map(
            lambda state: (action, state, action.evaluate(current_state, state)),
            new_states,
        )
